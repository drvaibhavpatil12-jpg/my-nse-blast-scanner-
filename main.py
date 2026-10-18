from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Frontend connection enable karne ke liye

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "message": "Kotak Neo API Relay Ready"})

@app.route('/scan', methods=['POST'])
def scan_stocks():
    data = request.get_json() or {}
    
    # Dashboard se sirf consumer_key read hoga
    consumer_key = data.get('consumer_key')
    
    if not consumer_key:
        return jsonify({"error": "Consumer Key zaruri hai!"}), 400

    # Yahan aapka Kotak Neo API Data Fetching logic chalega
    return jsonify({
        "success": True,
        "message": "Live Data Fetched Successfully!",
        "data": []
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
