from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

# Kotak Neo REST Base URL
KOTAK_NEO_BASE_URL = "https://gw-napi.kotaksecurities.com"

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "message": "Kotak Neo Live API Service Online"})

@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    consumer_key = data.get('consumer_key')
    access_token = data.get('access_token')

    if not consumer_key or not access_token:
        return jsonify({
            "success": False, 
            "error": "Authentication Failed: Consumer Key aur Access Token dono zaruri hain!"
        }), 400

    try:
        # Direct Kotak Neo Live Quotes Endpoint
        headers = {
            "Authorization": f"Bearer {access_token}",
            "neo-fin-key": "neofin",
            "Content-Type": "application/json"
        }

        # Request Live Market Feed
        response = requests.get(
            f"{KOTAK_NEO_BASE_URL}/LiveFeed/1.0/quotes",
            headers=headers,
            timeout=8
        )

        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "Real Live Data Fetched Successfully!",
                "data": response.json()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Kotak Neo Server Response Code: {response.status_code}"
            }), response.status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Kotak Connection Exception: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
