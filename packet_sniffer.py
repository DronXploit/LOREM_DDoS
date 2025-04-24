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
        # Yo, where's the validation for target_ip? What if someone enters garbage?
        # Also, is_sniffing is set to False but never set to True anywhere. Dead flag much?
        
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
            # Another bare except? Seriously? What exceptions are you expecting here?
            # Maybe handle specific exceptions instead of catching everything?
            print(f"\033[91m [!] Error processing packet: {e}\033[91m")

    def start_sniffing(self):
        """Mulai sniffing dengan fallback jika Scapy tidak tersedia"""
        if not SCAPY_AVAILABLE:
            return self.start_limited_capture() 
            
        if os.geteuid() != 0:
            # At least you check for root. That's like the bare minimum for packet sniffing
            # But you're not telling users HOW to run as root. sudo python3 your_script.py, maybe?
            print("\033[91m[!] Error: Packet sniffing requires root privileges.\033[91m")
            return self.start_limited_capture()
        
        print(f"\033[92m[*] Starting scapy sniffing on {self.target_ip}...\033[92m")
        try:
            # You're only capturing packets TO the target, not FROM it
            # Real packet sniffers capture both directions, bro
            sniff(filter=f"dst host {self.target_ip}", 
                  prn=self.packet_callback, 
                  store=0,
                  stop_filter=lambda x: not self.is_sniffing)
        except Exception as e:
            # Third bare except. It's like you're collecting them
            print(f"\033[91m[!] Scapy error: {e}\033[91m")
            self.start_limited_capture()

    def start_limited_capture(self):
        """Fallback capture tanpa Scapy"""
        print("\033[93m[*] Starting limited packet capture (no Scapy)...\033[93m")
        try:
            import socket
            # Importing inside a function? That's not how imports work, my dude
            # Put this at the top with the other imports
            
            # SOCK_RAW with IPPROTO_TCP will only capture TCP packets
            # What about UDP? ICMP? Your "sniffer" is missing like 70% of traffic
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.bind(('0.0.0.0', 0))
            
            # Only capturing 20 packets? What kind of "sniffer" stops after 20 packets?
            # Wireshark is laughing at you right now
            print("\033[93m[*] Capturing first 20 packets (Press Ctrl+C to stop)...\033[93m")
            for _ in range(20):
                data = s.recvfrom(65565)
                # You're not even parsing the packet data, just printing the length
                # This is like a "sniffer" that just says "yep, that's a packet alright"
                print(f"\033[92m[Raw Packet] {len(data[0])} bytes from {data[1][0]}\033[92m")
        except Exception as e:
            # Fourth bare except. You're going for a record?
            print(f"\033[91m[!] Limited capture error: {e}\033[91m")
        finally:
            if 's' in locals():
                s.close()

    def stop_sniffing(self):
        # This function is never called from anywhere in the code
        # It's like buying a car and leaving it in the garage forever
        self.is_sniffing = False
        # Also, is_sniffing is never set to True, so this function does literally nothing
        # It's the coding equivalent of an appendix - vestigial and pointless