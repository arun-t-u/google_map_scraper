from flask import Flask, request, jsonify
from scraper.google_maps_scraper import GoogleMapsScraper

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    search_term = data.get("search_term")

    if not search_term:
        return jsonify({"error": "search_term is required"}), 400

    scraper = GoogleMapsScraper(search_term)
    results = scraper.run()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
