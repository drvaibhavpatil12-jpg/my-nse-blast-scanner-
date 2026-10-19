from flask import Flask, jsonify
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
    return jsonify({"status": "Backend Active", "provider": "Direct Live Feed - High Liquidity FNO"})

@app.route('/scan', methods=['GET', 'POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    try:
        # Top 30 High Liquidity & High Beta F&O Stocks for Intraday Moves
        tickers_map = {
            "^NSEI": "NIFTY 50",
            "^NSEBANK": "BANK NIFTY",
            # Banking & Financials (Heavy Movers)
            "HDFCBANK.NS": "HDFCBANK",
            "ICICIBANK.NS": "ICICIBANK",
            "AXISBANK.NS": "AXISBANK",
            "SBIN.NS": "SBIN",
            "KOTAKBANK.NS": "KOTAKBANK",
            "BAJFINANCE.NS": "BAJFINANCE",
            "BAJAJFINSV.NS": "BAJAJFINSV",
            # Auto & Infrastructure
            "TATAMOTORS.NS": "TATAMOTORS",
            "M&M.NS": "M&M",
            "MARUTI.NS": "MARUTI",
            "LT.NS": "LT",
            # Energy, Metals & Oil
            "RELIANCE.NS": "RELIANCE",
            "TATASTEEL.NS": "TATASTEEL",
            "HINDALCO.NS": "HINDALCO",
            "JSWSTEEL.NS": "JSWSTEEL",
            "COALINDIA.NS": "COALINDIA",
            # IT & Tech (High Volatility)
            "INFY.NS": "INFY",
            "TCS.NS": "TCS",
            "TECHM.NS": "TECHM",
            "WIPRO.NS": "WIPRO",
            # Telecom, FMCG & Consumer
            "BHARTIARTL.NS": "BHARTIARTL",
            "ITC.NS": "ITC",
            "TITAN.NS": "TITAN",
            # High Beta & Momentum Stocks
            "ADANIENT.NS": "ADANIENT",
            "ADANIPORTS.NS": "ADANIPORTS",
            "BEL.NS": "BEL",
            "HAL.NS": "HAL",
            "DLF.NS": "DLF",
            "REC.NS": "REC",
            "PFC.NS": "PFC"
        }

        symbols_list = list(tickers_map.keys())
        # Fetching bulk data in single call for high performance
        data = yf.download(symbols_list, period="2d", interval="1m", progress=False)

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

        # Sort stocks by Percentage Change (Highest Gainers / Losers on top)
        parsed_data.sort(key=lambda x: x['chg'], reverse=True)

        return jsonify({"success": True, "data": parsed_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
