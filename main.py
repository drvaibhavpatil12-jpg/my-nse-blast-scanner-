import os
from flask import Flask, jsonify

app = Flask(__name__)

# Kotak Neo API credentials (Render environment variables se safe rahengi)
CONSUMER_KEY = os.environ.get('KOTAK_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('KOTAK_CONSUMER_SECRET')

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "NSE Blast Scanner Backend is running securely!"
    })

@app.route('/api/scan-data')
def scan_data():
    return jsonify({
        "scanner_status": "Active",
        "data_source": "Kotak Neo Secure Backend",
        "stocks": [
            {"symbol": "RELIANCE", "ltp": 2755.00, "status": "PDH Breakout"},
            {"symbol": "INFY", "ltp": 1420.00, "status": "PDL Breakdown"}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
