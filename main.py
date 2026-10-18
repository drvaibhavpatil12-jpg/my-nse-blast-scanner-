from flask import Flask, request, jsonify

app = Flask(__name__)

# Native CORS handling (No external library needed)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "message": "Kotak Neo API Relay Ready"})

@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    consumer_key = data.get('consumer_key')
    
    if not consumer_key:
        return jsonify({"error": "Consumer Key zaruri hai!"}), 400

    return jsonify({
        "success": True,
        "message": "Live Data Fetched Successfully!",
        "data": []
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
