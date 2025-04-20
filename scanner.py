import asyncio
import ssl
from typing import List

class PortScanner:
    def __init__(self, host: str):
        self.host = host
        self.timeout = 1.5  # Timeout optimal
        self.max_concurrent = 500  # Batasan koneksi simultan

    async def _check_https(self, port: int) -> bool:
        """Optimized HTTPS detection with single attempt"""
        try:
            context = ssl.create_default_context()
            conn = asyncio.open_connection(
                host=self.host,
                port=port,
                ssl=context,
                server_hostname=self.host
            )
            reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False

    async def async_scan_port(self, port: int) -> int | None:
        """Optimized port scanning with smart detection"""
        try:
            # Coba koneksi TCP biasa dulu (lebih cepat untuk port non-HTTPS)
            conn = asyncio.open_connection(self.host, port)
            reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()

            # Jika TCP berhasil, cek apakah HTTPS
            is_https = await self._check_https(port)
            if is_https:
                print(f"\033[96m[+] Port {port} is OPEN (HTTPS)\033[0m")
            else:
                print(f"\033[92m[+] Port {port} is OPEN\033[0m")
            return port
        except:
            return None

    async def scan_ports(self, start_port: int, end_port: int) -> List[int]:
        """Optimized scan with controlled concurrency"""
        print(f"\033[94m[+] Scanning {self.host} (Port {start_port}-{end_port})...\033[0m")
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def limited_scan(port):
            async with semaphore:
                return await self.async_scan_port(port)

        tasks = [limited_scan(port) for port in range(start_port, end_port + 1)]
        results = await asyncio.gather(*tasks)
        
        open_ports = [port for port in results if port is not None]
        print(f"\033[94m[+] Scan completed. Found {len(open_ports)} open ports.\033[0m")
        return open_ports
