import streamlit as st
from datetime import datetime
import hashlib
import json
import pandas as pd
import matplotlib.pyplot as plt
from hashlib import sha256

# ----- Classe Block -----
class Block:
    def __init__(self, index, sender, receiver, amount, fee, previous_hash, balances, nonce=0):
        self.index = index
        self.timestamp = datetime.now()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.previous_hash = previous_hash
        self.balances = balances.copy()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "fee": self.fee,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        return sha256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

# ----- Blockchain Class -----
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.target_block_time = 10  # Target time in seconds
        self.adjustment_interval = 5  # Adjust every 5 blocks
        self.users = {
            "Chouaib": 100,
            "Achraf Selougha": 50,
            "Benamrane Achraf": 75,
            "System": float('inf')
        }
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "System", "Genesis", 0, 0, "0", self.users)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def adjust_difficulty(self):
        if len(self.chain) % self.adjustment_interval == 0 and len(self.chain) > 1:
            last_adjustment_block = self.chain[-self.adjustment_interval]
            last_block = self.get_last_block()
            time_taken = (last_block.timestamp - last_adjustment_block.timestamp).total_seconds()
            expected_time = self.adjustment_interval * self.target_block_time
            ratio = time_taken / expected_time
            if ratio < 0.5:  # Mining too fast
                self.difficulty += 1
            elif ratio > 2:  # Mining too slow
                self.difficulty = max(1, self.difficulty - 1)
            st.info(f"Difficulty adjusted to {self.difficulty}")

    def add_block(self, sender, receiver, amount, fee=0.1):
        if sender not in self.users or receiver not in self.users:
            raise ValueError("Invalid sender or receiver")
        if sender == receiver:
            raise ValueError("Sender and receiver must be different")
        total_cost = amount + fee
        if self.get_last_block().balances[sender] < total_cost:
            raise ValueError("Insufficient balance for amount and fee")
        
        new_balances = self.get_last_block().balances.copy()
        new_balances[sender] -= total_cost
        new_balances[receiver] += amount
        new_balances["System"] += fee  # Fee goes to the system (miner)
        
        new_block = Block(
            index=len(self.chain),
            sender=sender,
            receiver=receiver,
            amount=amount,
            fee=fee,
            previous_hash=self.get_last_block().hash,
            balances=new_balances
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.adjust_difficulty()  # Adjust difficulty after adding block
        return new_block

    def get_last_block(self):
        return self.chain[-1]
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# ----- Initialize Blockchain -----
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# ----- Helper Functions -----
def display_block(block):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Block Index", block.index)
        st.metric("Amount", f"{block.amount} $")
        st.metric("Fee", f"{block.fee} $")
    with col2:
        st.write(f"**Timestamp:** {block.timestamp}")
        st.write(f"**Sender:** {block.sender}")
        st.write(f"**Receiver:** {block.receiver}")
        st.write(f"**Previous Hash:** `{block.previous_hash[:20]}...`")
        st.write(f"**Current Hash:** `{block.hash[:20]}...`")
        st.write(f"**Nonce:** {block.nonce}")
    
    st.write("**Balances after transaction:**")
    balances_df = pd.DataFrame(list(block.balances.items()), columns=["User", "Balance"])
    st.dataframe(balances_df.style.highlight_max(axis=0, subset=["Balance"], color='lightgreen'), 
                 use_container_width=True)

def plot_balance_history():
    history = []
    for block in st.session_state.blockchain.chain:
        history.append({
            "block": block.index,
            **block.balances
        })
    
    df = pd.DataFrame(history).set_index("block")
    df = df.drop("System", axis=1)  # Remove System from plot
    
    fig, ax = plt.subplots(figsize=(10, 5))
    for user in df.columns:
        ax.plot(df.index, df[user], marker='o', label=user)
    
    ax.set_title("Balance Evolution Over Blocks")
    ax.set_xlabel("Block Number")
    ax.set_ylabel("Balance ($)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# ----- Streamlit UI -----
st.set_page_config(page_title="Blockchain Payment System", layout="wide")
st.title("🔗 Blockchain Payment System Simulation")

# Sidebar for settings and transaction history
with st.sidebar:
    st.header("⚙️ Blockchain Settings")
    st.session_state.blockchain.difficulty = st.slider("Initial Mining Difficulty", 1, 6, 4)
    if st.button("🔄 Reset Blockchain"):
        st.session_state.blockchain = Blockchain()
        st.success("Blockchain reset to genesis block!")
    
    st.header("ℹ️ Blockchain Info")
    st.write(f"**Chain Length:** {len(st.session_state.blockchain.chain)} blocks")
    st.write(f"**Chain Valid:** {'✅ Yes' if st.session_state.blockchain.is_chain_valid() else '❌ No'}")
    st.write(f"**Current Difficulty:** {st.session_state.blockchain.difficulty}")
    st.write(f"**Mining Target:** {'0' * st.session_state.blockchain.difficulty}...")
    
    st.header("📜 Transaction History")
    for block in st.session_state.blockchain.chain[::-1]:  # Reverse to show newest first
        if block.index == 0:  # Skip genesis block
            continue
        with st.expander(f"Block #{block.index} - {block.timestamp.strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(f"**From:** {block.sender}")
            st.markdown(f"**To:** {block.receiver}")
            st.markdown(f"**Amount:** {block.amount} $")
            st.markdown(f"**Fee:** {block.fee} $")
            st.markdown("**Balances after transaction:**")
            balances_df = pd.DataFrame(list(block.balances.items()), columns=["User", "Balance"])
            st.dataframe(balances_df, use_container_width=True)

# Main content
tab1, tab2, tab3 = st.tabs(["💰 Make Transaction", "📊 Blockchain Explorer", "📈 Analytics"])

with tab1:
    st.subheader("💸 Make a Transaction")
    col1, col2 = st.columns(2)
    
    with col1:
        sender = st.selectbox("Sender:", [u for u in st.session_state.blockchain.users.keys() if u != "System"])
        receiver = st.selectbox("Receiver:", [u for u in st.session_state.blockchain.users.keys() if u != sender and u != "System"])
    
    with col2:
        amount = st.number_input("Amount ($):", min_value=1, step=1)
        fee = st.number_input("Transaction Fee ($):", min_value=0.1, value=0.1, step=0.1)
        current_balance = st.session_state.blockchain.get_last_block().balances.get(sender, 0)
        st.write(f"**Current Balance:** {current_balance} $")
        
        if amount + fee > current_balance:
            st.warning("⚠️ Amount + Fee exceeds current balance!")
            st.button("⛏️ Mine Transaction", disabled=True)
        else:
            if st.button("⛏️ Mine Transaction"):
                try:
                    new_block = st.session_state.blockchain.add_block(sender, receiver, amount, fee)
                    st.success(f"✅ Transaction mined successfully in Block #{new_block.index}!")
                    st.balloons()
                except ValueError as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("🔍 Blockchain Explorer")
    
    selected_block = st.selectbox(
        "Select Block to Inspect:",
        options=range(len(st.session_state.blockchain.chain)),
        format_func=lambda x: f"Block #{x} - {st.session_state.blockchain.chain[x].timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    block = st.session_state.blockchain.chain[selected_block]
    display_block(block)
    
    with st.expander("📄 View Raw Block Data"):
        block_data = {
            "index": block.index,
            "timestamp": str(block.timestamp),
            "sender": block.sender,
            "receiver": block.receiver,
            "amount": block.amount,
            "fee": block.fee,
            "previous_hash": block.previous_hash,
            "hash": block.hash,
            "nonce": block.nonce,
            "balances": block.balances
        }
        st.json(block_data)

with tab3:
    st.subheader("📊 Blockchain Analytics")
    
    st.write("### Balance History")
    plot_balance_history()
    
    st.write("### Recent Transactions")
    recent_txs = []
    for block in st.session_state.blockchain.chain[-10:][::-1]:
        if block.index == 0:
            continue
        recent_txs.append({
            "Block": block.index,
            "From": block.sender,
            "To": block.receiver,
            "Amount": f"{block.amount} $",
            "Fee": f"{block.fee} $",
            "Timestamp": block.timestamp.strftime("%Y-%m-%d %H:%M")
        })
    
    if recent_txs:
        st.table(recent_txs)
    else:
        st.info("No transactions yet. Make your first transaction in the 'Make Transaction' tab.")

# Footer
st.markdown("---")
st.markdown("""
    *This is an advanced blockchain simulation demonstrating core concepts like blocks, hashing, mining, and transaction validation.*
    - **Dynamic Difficulty Adjustment**: Mimics Bitcoin's difficulty adjustment to maintain stable block times.
    - **Transaction Fees**: Simulates real-world blockchain economics with miner incentives.
    - **Proof-of-Work**: Requires computational work to mine blocks, ensuring security.
    - **Chain Validation**: Ensures integrity by verifying hashes and previous hash references.
""")