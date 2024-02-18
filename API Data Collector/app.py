#pip install python-dotenv
#pip install Flask

#Style more w stylin'

import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

# initialize flask application
load_dotenv()
app = Flask(__name__)

#pull boba data from yelp api with api key
def get_boba_spots(location):
    apiKey = os.environ.get("yelp_api_key")
    headers = {"Authorization": f"Bearer {apiKey}"}
    params = {
        "term": "boba",
        "location": location,
        "limit": 5
    }

    response = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    if response.status_code == 200:
        businesses = response.json()["businesses"]
        boba_spots = []
        for shop in businesses:
            boba_spots.append({
                'name': shop['name'],
                'rating': shop['rating'],
                'image_url': shop['image_url']
            })
        return boba_spots
    else:
        print("Failed to fetch data from Yelp API. Status Code:", response.status_code)
        return None

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route for Search Request
@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    boba_spots = get_boba_spots(location)
    return render_template('results.html', boba_spots=boba_spots, location=location)

# Start Flask App
if __name__ == '__main__':
    app.run(debug=True)