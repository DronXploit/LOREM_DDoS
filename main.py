#!/usr/bin/env python3
import argparse
import asyncio
import sys
import signal
import time
from urllib.parse import urlparse
from datetime import datetime
from scanner import PortScanner
from packet_sniffer import PacketSniffer
from api_checker import APIChecker
from ddos_attacker import AdvancedDDoSAttacker

def sanitize_host_input(raw_input):
    parsed = urlparse(raw_input if "://" in raw_input else f"http://{raw_input}")
    return parsed.hostname

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
                ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝  VERSION: 3.0            
    ===========================================================
      Author              : dronXploit
      Contributor         : palacita135
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
                return sanitize_host_input(target)
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

    def get_thread_count(self) -> int:
        while True:
            try:
                threads = int(input(Colors.colorize("Jumlah threads (50-1000): ", Colors.BOLD)).strip())
                if 50 <= threads <= 10000:
                    return threads
                print(Colors.colorize("[!] Masukkan angka antara 50-1000", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Input harus angka", Colors.RED))
    
    def get_duration(self) -> int:
        while True:
            try:
                duration = int(input(Colors.colorize("Duration (seconds): ", Colors.BOLD)).strip())
                if duration > 0:
                    return duration
                print(Colors.colorize("[!] Duration harus lebih dari 0", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Input harus angka", Colors.RED))

    def _confirm_attack(self):
        """Get user confirmation before attack"""
        confirm = input(Colors.colorize("Apakah Anda yakin ingin melanjutkan serangan? (y/n): ", Colors.BOLD)).strip().lower()
        return confirm == 'y'
    
    def _select_port(self, open_ports: list) -> int:
        """Port selection logic"""
        while True:
            try:
                choice = input(Colors.colorize("Select port to attack (number): ", Colors.BOLD))
                idx = int(choice) - 1
                if 0 <= idx < len(open_ports):
                    return open_ports[idx]
                print(Colors.colorize("[!] Invalid number", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Must be a number", Colors.RED))

    def _get_duration(self) -> int:
        """Get duration from user"""
        while True:
            try:
                duration = int(input(Colors.colorize("Durasi (detik): ", Colors.BOLD)).strip())
                if duration > 0:
                    return duration
                print(Colors.colorize("[!] Durasi harus lebih dari 0", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Input harus angka", Colors.RED))

    def _get_thread_count(self) -> int:
        """Get number of threads from user"""
        while True:
            try:
                threads = int(input(Colors.colorize("Jumlah threads (50-1000): ", Colors.BOLD)).strip())
                if 50 <= threads <= 10000:
                    return threads
                print(Colors.colorize("[!] Masukkan angka antara 50-1000", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Input harus angka", Colors.RED))

    def _show_attack_results(self, stats: dict):
        """Display final attack statistics"""
        print(Colors.colorize("\n[+] ATTACK COMPLETED", Colors.BOLD + Colors.GREEN))
        print(Colors.colorize(f"Duration: {stats['duration']}", Colors.CYAN))
        print(Colors.colorize(f"Total Requests: {stats['total_requests']:,}", Colors.CYAN))
        print(Colors.colorize(f"Successful: {stats['success_requests']:,}", Colors.GREEN))
        print(Colors.colorize(f"Failed: {stats['failed_requests']:,}", Colors.RED))
        print(Colors.colorize(f"Requests/sec: {stats['requests_per_sec']:,.1f}", Colors.CYAN))
        print(Colors.colorize(f"Bandwidth Used: {stats['bandwidth_mb']:.2f} MB", Colors.CYAN))

    def _select_attack_type(self, target: str) -> str:
        """Attack type selection"""
        print(Colors.colorize("\n[ATTACK TYPES]", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize("1. SYN Flood (Network Layer)", Colors.GREEN))
        print(Colors.colorize("2. HTTP Flood (Application Layer)", Colors.GREEN))
        print(Colors.colorize("3. SSL Flood (Encrypted Attack)", Colors.GREEN))
    
        while True:
            choice = input(Colors.colorize("Select attack type (1-3): ", Colors.BOLD))
            if choice == '1':
                return 'syn'
            elif choice == '2':
                return 'http'
            elif choice == '3':
                return 'ssl'
            print(Colors.colorize("[!] Invalid choice", Colors.RED))

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
        print(Colors.colorize("\n[ADVANCED DDoS TOOL]", Colors.BOLD + Colors.RED))
        target = self.get_target_input("Masukkan target (IP/Domain: ")

        print(Colors.colorize("[*] Scanning target ports...", Colors.YELLOW))
        scanner = PortScanner(target)
        try:
            open_ports = asyncio.run(scanner.scan_ports(1, 10000))  # Scan more ports
            if not open_ports:
                print(Colors.colorize("[!] No open ports found", Colors.RED))
                return

            print(Colors.colorize("[+] Open ports found:", Colors.GREEN))
            for i, port in enumerate(open_ports[:20], 1):  # Show first 20 ports
                print(Colors.colorize(f"{i}. Port {port}", Colors.GREEN))
        
            port = self._select_port(open_ports)
            attack_type = self._select_attack_type(target)
            threads = self._get_thread_count()
            duration = self._get_duration()
            

            print(Colors.colorize("\n[!] ATTACK CONFIGURATION:", Colors.BOLD + Colors.RED))
            print(Colors.colorize(f"Target: {target}:{port}", Colors.YELLOW))
            print(Colors.colorize(f"Attack Type: {attack_type.upper()}", Colors.YELLOW))
            print(Colors.colorize(f"Threads: {threads}", Colors.YELLOW))
            print(Colors.colorize(f"Duration: {duration} seconds", Colors.YELLOW))
        
            if not self._confirm_attack():
                print(Colors.colorize("[!] Attack canceled", Colors.YELLOW))
                return
            
            print(Colors.colorize("[*] Starting attack...", Colors.YELLOW))

            self._execute_attack(target, port, attack_type, threads, duration)

            attacker = AdvancedDDoSAttacker(target, port, threads)
            try:
                attacker.start_attack(attack_type)
        
                # Progress display
                start_time = time.time()
                while time.time() - start_time < duration:
                    remaining = int(duration - (time.time() - start_time))
                    time_left = int(duration - (time.time() - start_time))
                    print(Colors.colorize(
                        f"\r[*] Attacking... Time left: {time_left}s | " 
                        f"Requests: {attacker.stats['total_requests']} | "
                        f"Success: {attacker.stats['success_requests']}", 
                        Colors.YELLOW), end='')
                    time.sleep(1)
            except KeyboardInterrupt:
                print(Colors.colorize("\n[!] Attack stopped manually", Colors.YELLOW))
            finally:
                stats = attacker.stop_attack()
                self._show_attack_results(stats)

        except Exception as e:
            print(Colors.colorize(f"[!] Error: {str(e)}", Colors.RED))

    def _select_port(self, open_ports):
        """Port selection logic"""
        while True:
            try:
                choice = input(Colors.colorize("Select port to attack (number): ", Colors.BOLD))
                idx = int(choice) - 1
                if 0 <= idx < len(open_ports):
                    return open_ports[idx]
                print(Colors.colorize("[!] Invalid number", Colors.RED))
            except ValueError:
                print(Colors.colorize("[!] Must be a number", Colors.RED))

    def _select_attack_type(self, target):
        """Attack type selection"""
        print(Colors.colorize("\n[ATTACK TYPES]", Colors.BOLD + Colors.CYAN))
        print(Colors.colorize("1. SYN Flood (Network Layer)", Colors.GREEN))
        print(Colors.colorize("2. HTTP Flood (Application Layer)", Colors.GREEN))
        print(Colors.colorize("3. SSL Flood (Encrypted Attack)", Colors.GREEN))
    
        while True:
            choice = input(Colors.colorize("Select attack type (1-3): ", Colors.BOLD))
            if choice == '1':
                return 'syn'
            elif choice == '2':
                return 'http'
            elif choice == '3':
                return 'ssl'
            print(Colors.colorize("[!] Invalid choice", Colors.RED))

    def _execute_attack(self, target, port, attack_type, threads, duration):
        """Execute the actual attack"""
        print(Colors.colorize("\n[!] LAUNCHING ATTACK...", Colors.BOLD + Colors.RED))
    
        attacker = AdvancedDDoSAttacker(target, port, threads)
        try:
            attacker.start_attack(attack_type)
        
            # Progress display
            start_time = time.time()
            while time.time() - start_time < duration:
                time_left = int(duration - (time.time() - start_time))
                print(Colors.colorize(
                    f"\r[*] Attacking... Time left: {time_left}s | " 
                    f"Requests: {attacker.stats['total_requests']} | "
                    f"Success: {attacker.stats['success_requests']}", 
                    Colors.YELLOW), end='')
                time.sleep(1)
            
        except KeyboardInterrupt:
            print(Colors.colorize("\n[!] Attack stopped manually", Colors.YELLOW))
        finally:
            stats = attacker.stop_attack()
            self._show_attack_results(stats)

    def _show_attack_results(self, stats):
        """Display final attack statistics"""
        print(Colors.colorize("\n[+] ATTACK COMPLETED", Colors.BOLD + Colors.GREEN))
        print(Colors.colorize(f"Duration: {stats['duration']}", Colors.CYAN))
        print(Colors.colorize(f"Total Requests: {stats['total_requests']:,}", Colors.CYAN))
        print(Colors.colorize(f"Successful: {stats['success_requests']:,}", Colors.GREEN))
        print(Colors.colorize(f"Failed: {stats['failed_requests']:,}", Colors.RED))
        print(Colors.colorize(f"Requests/sec: {stats['requests_per_sec']:,.1f}", Colors.CYAN))
        print(Colors.colorize(f"Bandwidth Used: {stats['bandwidth_mb']:.2f} MB", Colors.CYAN))
    
    def run_packet_sniffer(self):
        print(Colors.colorize("\n[PACKET SNIFFER]", Colors.BOLD + Colors.CYAN))
        target = self.get_target_input("Masukkan target (IP/Domain: ")
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
