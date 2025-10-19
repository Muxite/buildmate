import requests


def perform_search(query, base_url="http://localhost:5000/search"):
    """
    Performs a real search by calling the Flask /search API endpoint.

    Args:
        query (str): The search query string.
        base_url (str): URL of the search API endpoint.

    Returns:
        list[dict]: List of search results containing 'uri', 'title', and 'snippet'.
    """
    if not query:
        raise ValueError("Query cannot be empty")

    try:
        response = requests.get(base_url, params={"q": query})
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
        data = response.json()
        if "result" not in data:
            raise ValueError("Unexpected API response format")
        return data["result"]
    except requests.RequestException as e:
        print(f"[ERROR] Failed to perform search: {e}")
        return []
