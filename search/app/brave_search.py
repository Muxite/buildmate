import requests
import time

class BraveSearch:
    def __init__(self, api_key: str, max_retries: int = 3, backoff_factor: float = 2.0):
        self.api_key = api_key
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    def search(self, query: str, count: int = 10, search_lang: str = "en", country: str = None, **kwargs) -> str:
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        payload = {
            "q": query,
            "count": count,
            "search_lang": search_lang
        }
        if country:
            payload["country"] = country
        payload.update(kwargs)

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.get(self.base_url, headers=headers, params=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return self._extract_text(data)
                else:
                    print(f"[Attempt {attempt}] Status {resp.status_code}: {resp.text}")
            except requests.RequestException as e:
                print(f"[Attempt {attempt}] Request Exception: {e}")
            time.sleep(self.backoff_factor ** attempt)

        return "Failed to retrieve search results after multiple attempts."

    def _extract_text(self, data: dict) -> str:
        web_results = data.get("web", {}).get("results", [])
        if not web_results:
            return "No search results found."

        texts = []
        for r in web_results[:10]:
            title = r.get("title", "")
            snippet = r.get("description", "") or r.get("snippet", "")
            url = r.get("url", "")
            texts.append(f"{title}\n{snippet}\nURL: {url}\n")
        return "\n---\n".join(texts)