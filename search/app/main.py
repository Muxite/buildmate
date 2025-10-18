from flask import Flask, request, jsonify
from brave_search import BraveSearch
import os

app = Flask(__name__)
api_key = os.environ.get("SEARCH_API_KEY")
if not api_key:
    raise ValueError("BRAVE_API_KEY environment variable not set")

searcher = BraveSearch(api_key=api_key)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    result = searcher.search(query)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)