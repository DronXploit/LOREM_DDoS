import sys
import os
try:
    from scapy.all import sniff, IP, TCP # type: ignore
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("\033[91m [!] Warning: Scapy not available, using limited packet capture\033[91m")

class PacketSniffer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.is_sniffing = False
        
    def packet_callback(self, packet):
        """Callback untuk processing packet"""
        try:
            if IP in packet and packet[IP].dst == self.target_ip:
                protocol = packet.sprintf("%IP.proto%")
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                if TCP in packet:
                    sport = packet[TCP].sport
                    dport = packet[TCP].dport
                    print(f"\033[92m[Sniffer] TCP Packet: {src_ip}:{sport} -> {dst_ip}:{dport}\033[92m")
                else:
                    print(f"\033[92m[Sniffer] Packet: {src_ip} -> {dst_ip} Protocol: {protocol}\033[92m")
        except Exception as e:
            print(f"\033[91m [!] Error processing packet: {e}\033[91m")

    def start_sniffing(self):
        """Mulai sniffing dengan fallback jika Scapy tidak tersedia"""
        if not SCAPY_AVAILABLE:
            return self.start_limited_capture()
            
        if os.geteuid() != 0:
            print("\033[91m[!] Error: Packet sniffing requires root privileges.\033[91m")
            return self.start_limited_capture()
        
        print(f"\033[92m[*] Starting scapy sniffing on {self.target_ip}...\033[92m")
        try:
            sniff(filter=f"dst host {self.target_ip}", 
                  prn=self.packet_callback, 
                  store=0,
                  stop_filter=lambda x: not self.is_sniffing)
        except Exception as e:
            print(f"\033[91m[!] Scapy error: {e}\033[91m")
            self.start_limited_capture()

    def start_limited_capture(self):
        """Fallback capture tanpa Scapy"""
        print("\033[93m[*] Starting limited packet capture (no Scapy)...\033[93m")
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.bind(('0.0.0.0', 0))
            
            print("\033[93m[*] Capturing first 20 packets (Press Ctrl+C to stop)...\033[93m")
            for _ in range(20):
                data = s.recvfrom(65565)
                print(f"\033[92m[Raw Packet] {len(data[0])} bytes from {data[1][0]}\033[92m")
        except Exception as e:
            print(f"\033[91m[!] Limited capture error: {e}\033[91m")
        finally:
            if 's' in locals():
                s.close()

    def stop_sniffing(self):
        self.is_sniffing = False