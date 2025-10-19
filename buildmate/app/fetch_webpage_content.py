import requests
from bs4 import BeautifulSoup


def fetch_webpage_content(url):
    """
    Fetches the plaintext content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: Plaintext content of the webpage.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse HTML and extract plaintext
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""
