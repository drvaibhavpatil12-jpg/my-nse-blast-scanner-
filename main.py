from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "provider": "Direct Live Feed"})

@app.route('/scan', methods=['GET', 'POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    try:
        # High Volume F&O Stocks List
        tickers_map = {
            "^NSEI": "NIFTY 50",
            "^NSEBANK": "BANK NIFTY",
            "RELIANCE.NS": "RELIANCE",
            "HDFCBANK.NS": "HDFCBANK",
            "ICICIBANK.NS": "ICICIBANK",
            "AXISBANK.NS": "AXISBANK",
            "SBIN.NS": "SBIN",
            "BAJFINANCE.NS": "BAJFINANCE",
            "TATAMOTORS.NS": "TATAMOTORS",
            "M&M.NS": "M&M",
            "MARUTI.NS": "MARUTI",
            "LT.NS": "LT",
            "TATASTEEL.NS": "TATASTEEL",
            "HINDALCO.NS": "HINDALCO",
            "INFY.NS": "INFY",
            "TCS.NS": "TCS",
            "BHARTIARTL.NS": "BHARTIARTL",
            "ADANIENT.NS": "ADANIENT",
            "HAL.NS": "HAL",
            "BEL.NS": "BEL"
        }

        symbols_list = list(tickers_map.keys())
        # Downloading fast 1d data for quick response
        data = yf.download(symbols_list, period="2d", interval="5m", progress=False, timeout=10)

        parsed_data = []

        for ticker in symbols_list:
            try:
                stock_df = data['Close'][ticker].dropna()
                if len(stock_df) >= 2:
                    current_price = float(stock_df.iloc[-1])
                    prev_close = float(stock_df.iloc[0])
                    change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)
                    
                    parsed_data.append({
                        "symbol": tickers_map[ticker],
                        "ltp": round(current_price, 2),
                        "chg": change_pct
                    })
            except Exception:
                continue

        parsed_data.sort(key=lambda x: x['chg'], reverse=True)

        return jsonify({"success": True, "data": parsed_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
