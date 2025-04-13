import requests

class APIChecker:
    def __init__(self, url):
        self.url = url

    def check_api(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                print(f"\033[92m[+]API ditemukan: {self.url} (Status: {response.status_code})\033[0m")
                print(f"\033[92m Response: {response.json()}\033[0m")
            else:
                print(f"\033[92m[-]API {self.url} returned status code: {response.status_code}\033[0m")
        except Exception as e:
            print(f"\033[91m[-]Error checking API {self.url}: {e}\033[91m")

    def is_rate_limit_disabled(self):
        try:
            for _ in range (10):
                requests.get(self.url)
                return True
        except:
            print(f"\033[91m[+] Rate limit tidak diaktifkan untuk API {self.url}\033[91m")
            print(f"\033[91m[-]Rate limit diaktifkan untuk API {self.url}\033[91m")
            print(f"\033[91m[-]Error checking rate limit for API {self.url}\033[91m")
            print(f"\033[91m[-]Rate limit diaktifkan untuk API {self.url}\033[91m")
            return False