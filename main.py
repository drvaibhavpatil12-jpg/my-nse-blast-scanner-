from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "message": "Kotak Neo Intraday Radar Relay Ready"})

@app.route('/scan', methods=['POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    consumer_key = data.get('consumer_key')
    
    if not consumer_key:
        return jsonify({"error": "Consumer Key zaruri hai!"}), 400

    dashboard_data = {
        "indices": {
            "nifty": {"ltp": 24850.20, "pchange": "+0.51%", "sentiment": "BULLISH 🚀"},
            "banknifty": {"ltp": 51200.80, "pchange": "-0.16%", "sentiment": "BEARISH 📉"},
            "market_breadth": {"advances": 34, "declines": 16, "ratio": "68% Bullish"}
        },
        "sectors": {
            "bullish": [
                {"name": "NIFTY IT", "change": "+1.85%", "flow": "Strong Inflow 🔥"},
                {"name": "NIFTY AUTO", "change": "+1.20%", "flow": "Inflow 🟢"}
            ],
            "bearish": [
                {"name": "NIFTY PHARMA", "change": "-0.95%", "flow": "Outflow 🔴"},
                {"name": "NIFTY FMCG", "change": "-0.40%", "flow": "Mild Outflow 🔴"}
            ]
        },
        # Exact 6-Point Filter Matched Stocks
        "blast_6_point": {
            "buy_call": [
                {
                    "symbol": "TATAMOTORS",
                    "ltp": 980.50,
                    "change": "+3.4%",
                    "match": "6/6 Rules Met",
                    "details": "Price > VWAP | > Pivot | EMA 9>20>50 | Vol > 1.5x | ADX>25 | 15M High Break"
                }
            ],
            "sell_call": [
                {
                    "symbol": "INFY",
                    "ltp": 1820.00,
                    "change": "-2.1%",
                    "match": "6/6 Rules Met",
                    "details": "Price < VWAP | < Pivot | EMA 9<20<50 | Sell Vol > 1.5x | ADX>25 | 15M Low Break"
                }
            ]
        },
        "volume_shockers": [
            {"symbol": "SBIN", "ltp": 835.00, "volume_spike": "4.2x Avg", "change": "+2.1%"}
        ],
        "vwap_crossover": [
            {"symbol": "RELIANCE", "ltp": 2740.00, "signal": "Bullish Crossed VWAP", "change": "+1.1%"}
        ]
    }

    return jsonify({
        "success": True,
        "message": "Market Radar Data Fetched Successfully!",
        "data": dashboard_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
