import socket
from concurrent.futures import ThreadPoolExecutor
import asyncio

class PortScanner:
    def __init__(self, host):
        self.host = host

    async def async_scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            await asyncio.get_event_loop().sock_connect(sock, (self.host, port))
            print(f"\033[92m[+] Port {port} is OPEN\033[0m")
            sock.close()
            return port
        except:
            return None

    async def scan_ports(self, start_port, end_port):
        print(f"\033[92m[+] Scanning {self.host} (Port {start_port}-{end_port})...\033[0m")
        open_ports = []
        tasks = [self.async_scan_port(port) for port in range(start_port, end_port + 1)]
        results = await asyncio.gather(*tasks)
        open_ports = [port for port in results if port is not None]
        return open_ports