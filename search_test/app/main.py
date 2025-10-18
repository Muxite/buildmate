import os
import requests

SEARCH_URL = os.environ.get("SEARCH_URL", "http://search:5000/search")

def main():
    query = "OpenAI"
    try:
        resp = requests.get(SEARCH_URL, params={"q": query}, timeout=5)
        if resp.status_code == 200:
            print("Search service responded successfully!")
            print(resp.json())
        else:
            print(f"Error: {resp.status_code}, {resp.text}")
    except Exception as e:
        print(f"Failed to connect to search service: {e}")

if __name__ == "__main__":
    main()
