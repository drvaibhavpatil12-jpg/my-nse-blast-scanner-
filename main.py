from flask import Flask, request, jsonify
from ks_api_client import ks_api
import os

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "message": "Live Kotak Neo Scanner Backend Ready"})

@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    
    # User-provided credentials
    consumer_key = data.get('consumer_key')
    consumer_secret = data.get('consumer_secret')
    access_token = data.get('access_token')
    session_token = data.get('session_token')

    if not consumer_key or not access_token:
        return jsonify({
            "success": False, 
            "error": "Authentication Failed: Consumer Key aur Access Token zaruri hain!"
        }), 400

    try:
        # Initialize Real Kotak Neo SDK Client
        client = ks_api.KSApiClient(
            access_token=access_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            app_id="NSE_BLAST_SCANNER"
        )

        # Login Session with Kotak Neo API
        client.session_2fa(access_token=session_token)

        # Live Market Feed Fetching for F&O Segment
        # Kotak Neo Scrip Quotes Endpoint
        quotes = client.quote(instrument_token=26000, quote_type="LTP") # Nifty 50 / F&O Quotes

        # Real Live Data Response
        return jsonify({
            "success": True,
            "message": "Real Live Market Data Fetched Successfully!",
            "data": quotes
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Kotak Neo Live API Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
