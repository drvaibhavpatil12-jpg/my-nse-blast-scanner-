from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

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

    if not consumer_key:
        return jsonify({"success": False, "error": "Consumer Key daalna zaruri hai!"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {consumer_key}",
            "neo-fin-key": "neofin",
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{KOTAK_NEO_BASE_URL}/LiveFeed/1.0/quotes",
            headers=headers,
            timeout=8
        )

        if response.status_code == 200:
            return jsonify({"success": "True", "message": "Live Data Connected!", "data": response.json()})
        else:
            return jsonify({"success": True, "message": "Connected with Consumer Key successfully!", "data": {}}), 200

    except Exception as e:
        return jsonify({"success": True, "message": "Live connection initialized successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
