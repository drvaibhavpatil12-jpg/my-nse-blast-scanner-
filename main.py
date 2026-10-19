from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({"status": "Backend Active", "provider": "Direct Live Feed - Full FNO"})

@app.route('/scan', methods=['GET', 'POST', 'OPTIONS'])
def scan_stocks():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    try:
        stocks_map = {
            "ADANIENSOL.NS": "ADANIENSOL", "GAIL.NS": "GAIL", "JSWENERGY.NS": "JSWENERGY", "NHPC.NS": "NHPC", "NTPC.NS": "NTPC",
            "ADANIGREEN.NS": "ADANIGREEN", "TATAPOWER.NS": "TATAPOWER", "ADANIPOWER.NS": "ADANIPOWER", "POWERGRID.NS": "POWERGRID",
            "ABCAPITAL.NS": "ABCAPITAL", "BAJAJHLDNG.NS": "BAJAJHLDNG", "BAJAJFINSV.NS": "BAJAJFINSV", "MUTHOOTFIN.NS": "MUTHOOTFIN",
            "MANAPPURAM.NS": "MANAPPURAM", "MCX.NS": "MCX", "BSE.NS": "BSE", "NAM-INDIA.NS": "NAM-INDIA", "360ONE.NS": "360ONE",
            "IREDA.NS": "IREDA", "INDUSINDBK.NS": "INDUSINDBK", "MOTILALOFS.NS": "MOTILALOFS", "SBICARD.NS": "SBICARD",
            "ANGELONE.NS": "ANGELONE", "HDFCAMC.NS": "HDFCAMC", "LTF.NS": "LTF", "AUBANK.NS": "AUBANK", "BANDHANBNK.NS": "BANDHANBNK",
            "LICI.NS": "LICI", "ICICIGI.NS": "ICICIGI", "PFC.NS": "PFC", "MFSL.NS": "MFSL", "RECLTD.NS": "RECLTD", "INDIANB.NS": "INDIANB",
            "HDFCLIFE.NS": "HDFCLIFE", "CDSL.NS": "CDSL", "JIOFIN.NS": "JIOFIN", "FEDERALBNK.NS": "FEDERALBNK", "IRFC.NS": "IRFC",
            "KOTAKBANK.NS": "KOTAKBANK", "IEX.NS": "IEX", "UNIONBANK.NS": "UNIONBANK", "CHOLAFIN.NS": "CHOLAFIN", "PNB.NS": "PNB",
            "HDFCBANK.NS": "HDFCBANK", "ICICIBANK.NS": "ICICIBANK", "IDFCFIRSTB.NS": "IDFCFIRSTB", "RBLBANK.NS": "RBLBANK",
            "YESBANK.NS": "YESBANK", "BAJFINANCE.NS": "BAJFINANCE", "SHRIRAMFIN.NS": "SHRIRAMFIN", "BANKINDIA.NS": "BANKINDIA",
            "AXISBANK.NS": "AXISBANK", "KFINTECH.NS": "KFINTECH", "SBIN.NS": "SBIN", "SBILIFE.NS": "SBILIFE", "PNBHOUSING.NS": "PNBHOUSING",
            "ICICIPRULI.NS": "ICICIPRULI", "CANBK.NS": "CANBK", "LICHSGFIN.NS": "LICHSGFIN", "BANKBARODA.NS": "BANKBARODA",
            "COCHINSHIP.NS": "COCHINSHIP", "CONCOR.NS": "CONCOR", "INDIGO.NS": "INDIGO", "ADANIPORTS.NS": "ADANIPORTS",
            "DELHIVERY.NS": "DELHIVERY", "SAIL.NS": "SAIL", "HINDZINC.NS": "HINDZINC", "NATIONALUM.NS": "NATIONALUM", "NMDC.NS": "NMDC",
            "JSWSTEEL.NS": "JSWSTEEL", "JINDALSTEL.NS": "JINDALSTEL", "TATASTEEL.NS": "TATASTEEL", "HINDALCO.NS": "HINDALCO",
            "COALINDIA.NS": "COALINDIA", "APLAPOLLO.NS": "APLAPOLLO", "VEDL.NS": "VEDL", "SIEMENS.NS": "SIEMENS", "ABB.NS": "ABB",
            "CUMMINSIND.NS": "CUMMINSIND", "CGPOWER.NS": "CGPOWER", "SUZLON.NS": "SUZLON", "BHEL.NS": "BHEL", "ASTRAL.NS": "ASTRAL",
            "SUPREMEIND.NS": "SUPREMEIND", "INOXWIND.NS": "INOXWIND", "BHARATFORG.NS": "BHARATFORG", "BDL.NS": "BDL",
            "SOLARINDS.NS": "SOLARINDS", "MAZDOCK.NS": "MAZDOCK", "POWERINDIA.NS": "POWERINDIA", "BEL.NS": "BEL", "HAL.NS": "HAL",
            "GLENMARK.NS": "GLENMARK", "SUNPHARMA.NS": "SUNPHARMA", "DRREDDY.NS": "DRREDDY", "AUROPHARMA.NS": "AUROPHARMA",
            "LAURUSLABS.NS": "LAURUSLABS", "CIPLA.NS": "CIPLA", "DIVISLAB.NS": "DIVISLAB", "TORNTPHARM.NS": "TORNTPHARM",
            "MANKIND.NS": "MANKIND", "ALKEM.NS": "ALKEM", "LUPIN.NS": "LUPIN", "ZYDUSLIFE.NS": "ZYDUSLIFE", "BIOCON.NS": "BIOCON",
            "ADANIENT.NS": "ADANIENT", "POLYCAB.NS": "POLYCAB", "VOLTAS.NS": "VOLTAS", "BLUESTARCO.NS": "BLUESTARCO", "AMBER.NS": "AMBER",
            "ASIANPAINT.NS": "ASIANPAINT", "KEI.NS": "KEI", "KAYNES.NS": "KAYNES", "HAVELLS.NS": "HAVELLS", "PGEL.NS": "PGEL",
            "WAAREEENER.NS": "WAAREEENER", "CROMPTON.NS": "CROMPTON", "DIXON.NS": "DIXON", "DALBHARAT.NS": "DALBHARAT",
            "GRASIM.NS": "GRASIM", "SHREECEM.NS": "SHREECEM", "LT.NS": "LT", "NBCC.NS": "NBCC", "ULTRACEMCO.NS": "ULTRACEMCO",
            "GMRAIRPORT.NS": "GMRAIRPORT", "AMBUJACEM.NS": "AMBUJACEM", "RVNL.NS": "RVNL", "APOLLOHOSP.NS": "APOLLOHOSP",
            "FORTIS.NS": "FORTIS", "MAXHEALTH.NS": "MAXHEALTH", "BAJAJ-AUTO.NS": "BAJAJ-AUTO", "EICHERMOT.NS": "EICHERMOT",
            "TVSMOTOR.NS": "TVSMOTOR", "TIINDIA.NS": "TIINDIA", "HEROMOTOCO.NS": "HEROMOTOCO", "ASHOKLEY.NS": "ASHOKLEY",
            "M&M.NS": "M&M", "FORCEMOT.NS": "FORCEMOT", "BOSCHLTD.NS": "BOSCHLTD", "SONACOMS.NS": "SONACOMS", "MARUTI.NS": "MARUTI",
            "DMART.NS": "DMART", "SWIGGY.NS": "SWIGGY", "TRENT.NS": "TRENT", "NAUKRI.NS": "NAUKRI", "NYKAA.NS": "NYKAA",
            "PATANJALI.NS": "PATANJALI", "MARICO.NS": "MARICO", "DABUR.NS": "DABUR", "HINDUNILVR.NS": "HINDUNILVR", "COLPAL.NS": "COLPAL",
            "BRITANNIA.NS": "BRITANNIA", "GODREJCP.NS": "GODREJCP", "NESTLEIND.NS": "NESTLEIND", "PAGEIND.NS": "PAGEIND",
            "TITAN.NS": "TITAN", "KALYANKJIL.NS": "KALYANKJIL", "SRF.NS": "SRF", "PIDILITIND.NS": "PIDILITIND", "UPL.NS": "UPL",
            "PIIND.NS": "PIIND", "TATACONSUM.NS": "TATACONSUM", "UNITDSPR.NS": "UNITDSPR", "GODFRYPHLP.NS": "GODFRYPHLP",
            "RADICO.NS": "RADICO", "ITC.NS": "ITC", "VBL.NS": "VBL", "WIPRO.NS": "WIPRO", "INFY.NS": "INFY", "HCLTECH.NS": "HCLTECH",
            "CAMS.NS": "CAMS", "MPHASIS.NS": "MPHASIS", "TECHM.NS": "TECHM", "PERSISTENT.NS": "PERSISTENT", "TCS.NS": "TCS",
            "OFSS.NS": "OFSS", "KPITTECH.NS": "KPITTECH", "TATAELXSI.NS": "TATAELXSI", "COFORGE.NS": "COFORGE", "PAYTM.NS": "PAYTM",
            "POLICYBZR.NS": "POLICYBZR", "DLF.NS": "DLF", "LODHA.NS": "LODHA", "GODREJPROP.NS": "GODREJPROP", "PRESTIGE.NS": "PRESTIGE",
            "PHOENIXLTD.NS": "PHOENIXLTD", "OBEROIRLTY.NS": "OBEROIRLTY", "IDEA.NS": "IDEA", "INDUSTOWER.NS": "INDUSTOWER",
            "BHARTIARTL.NS": "BHARTIARTL", "JUBLFOOD.NS": "JUBLFOOD", "INDHOTEL.NS": "INDHOTEL", "IOC.NS": "IOC", "HINDPETRO.NS": "HINDPETRO",
            "PETRONET.NS": "PETRONET", "OIL.NS": "OIL", "BPCL.NS": "BPCL", "ONGC.NS": "ONGC", "RELIANCE.NS": "RELIANCE"
        }

        sectors_map = {
            "^NSEI": "NIFTY 50", "^NSEBANK": "BANKNIFTY", "^CNXAUTO": "AUTO", "^CNXMETAL": "METAL",
            "^CNXIT": "IT", "^CNXPHARMA": "PHARMA", "^CNXFMCG": "FMCG", "^CNXREALTY": "REALTY",
            "^CNXENERGY": "ENERGY", "^CNXINFRA": "DEFENCE", "^CNXPSUBANK": "PSU BANK", "^CNXFINANCE": "FINANCE"
        }

        all_tickers = list(stocks_map.keys()) + list(sectors_map.keys())
        tickers_str = " ".join(all_tickers)
        
        # Download data directly as string for yfinance optimization
        data = yf.download(tickers_str, period="5d", interval="1d", progress=False, group_by='ticker', threads=True)

        parsed_stocks = []
        advance_count = 0
        decline_count = 0

        for ticker, name in stocks_map.items():
            try:
                if ticker in data:
                    df = data[ticker]['Close'].dropna()
                    if len(df) >= 2:
                        ltp = float(df.iloc[-1])
                        prev_close = float(df.iloc[-2])
                        chg = round(((ltp - prev_close) / prev_close) * 100, 2)

                        if chg > 0: advance_count += 1
                        elif chg < 0: decline_count += 1

                        parsed_stocks.append({
                            "symbol": name,
                            "ltp": round(ltp, 2),
                            "chg": chg,
                            "signal": "BUY" if chg >= 0 else "SELL"
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
                        prev_close = float(df.iloc[-2])
                        chg = round(((ltp - prev_close) / prev_close) * 100, 2)
                        sector_perf.append({"sector": name, "chg": chg})
            except Exception:
                continue

        sector_perf.sort(key=lambda x: x['chg'], reverse=True)
        parsed_stocks.sort(key=lambda x: x['chg'], reverse=True)

        return jsonify({
            "success": True,
            "advance": advance_count,
            "decline": decline_count,
            "sectors": sector_perf,
            "data": parsed_stocks
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
