# You need to install requests and beautifulsoup4 libraries first:
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import time

def scrape_headlines(url):
    """
    Scrape all h2 headlines from the specified URL
    """
    print(f"Scraping: {url}\n")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send HTTP GET request
        response = requests.get(url, headers=headers, timeout=10)
        # Raise exception if response status code is not 200
        response.raise_for_status()

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <h2> tags
        headlines = soup.find_all('h2')

        if not headlines:
            print("No <h2> headlines found.")
            return

        print("--- Found Headlines ---")
        for index, headline in enumerate(headlines, 1):
            # Clean text and print
            print(f"{index}. {headline.get_text(strip=True)}")
        print("------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unknown error occurred: {e}")


# Example: Scrape headlines from a news website
if __name__ == "__main__":
    # Use an example website with h2 tags
    scrape_headlines('http://pyclass.com/real-estate')