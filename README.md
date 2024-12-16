## Google Maps Scraper API

This project provides a simple API to scrape business details from Google Maps using Selenium and Flask. The scraper fetches business names and other details based on a search term and returns the data in JSON format.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.9+** (Tested with python 3.11)


## Running the Project Locally

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Install Chrome and ChromeDriver**

   - Download Chrome: [Google Chrome Download](https://www.google.com/chrome/)
   - Download ChromeDriver: [ChromeDriver Download](https://chromedriver.chromium.org/downloads)

   Ensure `chromedriver` is in your system's PATH.

3. **Run the Flask App**

   ```bash
   python run.py
   ```

4. **Send a Request to the API**

   ```bash
   curl -X POST http://localhost:5000/scrape \
   -H "Content-Type: application/json" \
   -d '{"search_term": "Garage doors in Los Angeles"}'
   ```
