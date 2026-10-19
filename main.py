from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active"})

@app.route('/scan', methods=['GET', 'POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    try:
        stocks_map = {
            "RELIANCE.NS": "RELIANCE", "TCS.NS": "TCS", "HDFCBANK.NS": "HDFCBANK", "ICICIBANK.NS": "ICICIBANK",
            "INFY.NS": "INFY", "SBIN.NS": "SBIN", "BHARTIARTL.NS": "BHARTIARTL", "LICI.NS": "LICI",
            "ITC.NS": "ITC", "KOTAKBANK.NS": "KOTAKBANK", "LT.NS": "LT", "AXISBANK.NS": "AXISBANK",
            "HINDUNILVR.NS": "HINDUNILVR", "BAJFINANCE.NS": "BAJFINANCE", "MARUTI.NS": "MARUTI", "SUNPHARMA.NS": "SUNPHARMA",
            "TITAN.NS": "TITAN", "ADANIENT.NS": "ADANIENT", "ULTRACEMCO.NS": "ULTRACEMCO", "ASIANPAINT.NS": "ASIANPAINT",
            "TATASTEEL.NS": "TATASTEEL", "NTPC.NS": "NTPC", "POWERGRID.NS": "POWERGRID", "M&M.NS": "M&M",
            "BAJAJFINSV.NS": "BAJAJFINSV", "WIPRO.NS": "WIPRO", "HCLTECH.NS": "HCLTECH", "ADANIPORTS.NS": "ADANIPORTS",
            "ONGC.NS": "ONGC", "COALINDIA.NS": "COALINDIA", "GRASIM.NS": "GRASIM", "JSWSTEEL.NS": "JSWSTEEL",
            "HINDALCO.NS": "HINDALCO", "TATAMOTORS.NS": "TATAMOTORS", "TECHM.NS": "TECHM", "BPCL.NS": "BPCL",
            "SBILIFE.NS": "SBILIFE", "CIPLA.NS": "CIPLA", "DRREDDY.NS": "DRREDDY", "BRITANNIA.NS": "BRITANNIA",
            "EICHERMOT.NS": "EICHERMOT", "DIVISLAB.NS": "DIVISLAB", "APOLLOHOSP.NS": "APOLLOHOSP", "HEROMOTOCO.NS": "HEROMOTOCO",
            "INDUSINDBK.NS": "INDUSINDBK", "SHRIRAMFIN.NS": "SHRIRAMFIN", "BAJAJ-AUTO.NS": "BAJAJ-AUTO", "BEL.NS": "BEL", "HAL.NS": "HAL"
        }

        sectors_map = {
            "^NSEI": "NIFTY 50", "^NSEBANK": "BANKNIFTY", "^CNXAUTO": "AUTO", "^CNXMETAL": "METAL",
            "^CNXIT": "IT", "^CNXPHARMA": "PHARMA", "^CNXFMCG": "FMCG", "^CNXREALTY": "REALTY",
            "^CNXENERGY": "ENERGY", "^CNXINFRA": "DEFENCE", "^CNXPSUBANK": "PSU BANK", "^CNXFINANCE": "FINANCE"
        }

        all_tickers = list(stocks_map.keys()) + list(sectors_map.keys())
        data = yf.download(all_tickers, period="2d", interval="1m", progress=False, group_by='ticker', threads=True)

        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist).strftime('%H:%M:%S')

        parsed_stocks = []
        advance_count = 0
        decline_count = 0

        for ticker, name in stocks_map.items():
            try:
                if ticker in data:
                    df = data[ticker]['Close'].dropna()
                    if len(df) >= 2:
                        ltp = float(df.iloc[-1])
                        prev_close = float(df.iloc[0])
                        chg = round(((ltp - prev_close) / prev_close) * 100, 2)

                        if chg > 0: advance_count += 1
                        elif chg < 0: decline_count += 1

                        parsed_stocks.append({
                            "symbol": name,
                            "ltp": round(ltp, 2),
                            "chg": chg,
                            "signal": "BUY" if chg >= 0 else "SELL",
                            "time": current_time
                        })
            except Exception:
                continue

        sector_perf = []
        for ticker, name in sectors_map.items():
            try:
                if ticker in data:
                    df = data[ticker]['Close'].dropna()
                    if len(df) >= 2:
                        ltp = float(df.iloc[-1])
                        prev_close = float(df.iloc[0])
                        chg = round(((ltp - prev_close) / prev_close) * 100, 2)
                        sector_perf.append({"sector": name, "chg": chg})
            except Exception:
                continue

        # Sort sectors High to Low
        sector_perf.sort(key=lambda x: x['chg'], reverse=True)
        
        # Sort stocks: Bullish low change on top (ascending), Bearish high drop on top
        bullish_stocks = sorted([s for s in parsed_stocks if s['chg'] >= 0], key=lambda x: x['chg'])
        bearish_stocks = sorted([s for s in parsed_stocks if s['chg'] < 0], key=lambda x: x['chg']) # most negative first

        final_stocks = bullish_stocks + bearish_stocks

        return jsonify({
            "success": True,
            "advance": advance_count,
            "decline": decline_count,
            "sectors": sector_perf,
            "data": final_stocks
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
