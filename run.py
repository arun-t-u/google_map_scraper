import pandas as pd
import io
from flask import Flask, request, jsonify, send_file
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
    df = pd.DataFrame(results)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='results.csv'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
