import requests

class APIChecker:
    def __init__(self, url):
        self.url = url
        # No URL validation? What if I pass "localhost" or an empty string?
        # Also no timeout setting? Enjoy waiting forever when an API doesn't respond

    def check_api(self):
        try:
            # No headers? No user agent? You're basically announcing "I'm a script!"
            # Most APIs will rate-limit or block you immediately
            response = requests.get(self.url)
            if response.status_code == 200:
                print(f"\033[92m[+]API ditemukan: {self.url} (Status: {response.status_code})\033[0m")
                print(f"\033[92m Response: {response.json()}\033[0m")
                # Calling .json() without checking if it's JSON first? What if it returns HTML?
                # Enjoy your JSONDecodeError, bro
            else:
                print(f"\033[92m[-]API {self.url} returned status code: {response.status_code}\033[0m")
                # Using green color (\033[92m) for error messages? 
                # Red is for errors, green is for success. Color coding 101, my dude
        except Exception as e:
            # At least you're catching exceptions, but like, maybe handle different types?
            # ConnectionError, Timeout, JSONDecodeError all mean different things
            print(f"\033[91m[-]Error checking API {self.url}: {e}\033[91m")

    def is_rate_limit_disabled(self):
        try:
            for _ in range (10):
                # Sending 10 requests with no delay between them?
                # That's not testing rate limits, that's just being rude to the API
                requests.get(self.url)
                # You're not even checking the response? What if it's returning 429 Too Many Requests?
                # You'd never know because you're ignoring the response completely
                return True
                # Wait, you're returning after the FIRST request? The loop is pointless!
                # It's like buying 10 pizzas but eating only one slice of the first one
        except:
            # Bare except? Again? What exceptions are you expecting here?
            # Also, you're printing FOUR different messages for the same error condition
            # Make up your mind, bro
            print(f"\033[91m[+] Rate limit tidak diaktifkan untuk API {self.url}\033[91m")
            # Using [+] for a negative result? And saying rate limit is NOT enabled when you caught an exception?
            # That's backwards logic, my dude
            print(f"\033[91m[-]Rate limit diaktifkan untuk API {self.url}\033[91m")
            # Wait, now you're saying rate limit IS enabled? Which is it?
            print(f"\033[91m[-]Error checking rate limit for API {self.url}\033[91m")
            # Now it's just an error? Make up your mind!
            print(f"\033[91m[-]Rate limit diaktifkan untuk API {self.url}\033[91m")
            # And you're repeating the same message twice? Ctrl+C, Ctrl+V much?
            return False
            # So any exception means rate limit is enabled? What if the server is down?
            # Or the URL is invalid? Or there's a network error?
            # All those would throw exceptions too, but have nothing to do with rate limits

# In conclusion:
# 1. Your rate limit check returns after the first request, making the loop pointless
# 2. You print contradictory messages saying rate limit is both enabled and disabled
# 3. You're not checking response codes, which is how rate limits are actually communicated
# 4. You're using color codes incorrectly (green for errors)
# 5. You're not validating the URL or setting timeouts
# 6. You're assuming all responses are JSON without checking
#
# This isn't an API checker, it's an exception generator with extra steps