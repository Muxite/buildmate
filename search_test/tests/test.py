import requests

url = 'http://localhost:5000/search'

params = {'q': 'python'}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Success:")
    print(response.json())
else:
    print(f"Failed with status code {response.status_code}: {response.text}")
