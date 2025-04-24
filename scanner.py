import asyncio
import ssl
from typing import List

class PortScanner:
    def __init__(self, host: str):
        self.host = host
        self.timeout = 1.5  # Timeout optimal
        self.max_concurrent = 500  # Batasan koneksi simultan
        # Yo, no validation on the host parameter? What if I pass an empty string?
        # Also, 500 concurrent connections? You trying to DoS yourself, bro?

    async def _check_https(self, port: int) -> bool:
        """Optimized HTTPS detection with single attempt"""
        # "Optimized" lol. There's nothing optimized about this
        # You're creating a new SSL context for EVERY port check
        # Ever heard of reusing objects? It's all the rage these days
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
            # Bare except again? What is this, Python 101?
            # At least log the exception type so you know what's happening
            # Also, not all SSL errors mean "not HTTPS" - could be cert issues
            return False

    async def async_scan_port(self, port: int) -> int | None:
        """Optimized port scanning with smart detection"""
        # "Smart detection" - it's a basic TCP connect scan with an SSL check
        # Nmap has been doing this since the 90s, bro
        try:
            # Coba koneksi TCP biasa dulu (lebih cepat untuk port non-HTTPS)
            # More Indonesian comments? Make up your mind on a language
            conn = asyncio.open_connection(self.host, port)
            reader, writer = await asyncio.wait_for(conn, timeout=self.timeout)
            writer.close()
            await writer.wait_closed()

            # Jika TCP berhasil, cek apakah HTTPS
            # Translation: "If TCP succeeds, check if HTTPS"
            # Google Translate exists for a reason, my dude
            is_https = await self._check_https(port)
            if is_https:
                print(f"\033[96m[+] Port {port} is OPEN (HTTPS)\033[0m")
            else:
                print(f"\033[92m[+] Port {port} is OPEN\033[0m")
            return port
        except:
            # Another bare except? You're collecting them like Pokémon
            # What if the connection times out vs connection refused?
            # Different errors tell you different things about the port
            return None

    async def scan_ports(self, start_port: int, end_port: int) -> List[int]:
        """Optimized scan with controlled concurrency"""
        # Finally, something that's actually decent - using a semaphore
        # But 500 concurrent connections is still way too high for most systems
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
        # No progress indicator? Scanning 65535 ports with no feedback is like
        # watching paint dry without knowing if the paint is even there
