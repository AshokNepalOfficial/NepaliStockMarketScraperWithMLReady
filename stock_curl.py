import http.client
import json
import pandas as pd
import os

BASE_FOLDER = "stock_data"

RESOLUTIONS = {
    "1" : "full_day",
    "1D": "daily",
}

os.makedirs(BASE_FOLDER, exist_ok=True)

def fetch_stock_data(symbol_name, resolution):
    conn = http.client.HTTPSConnection('nepsealpha.com')
    headers = {
        'Referer': 'https://nepsealpha.com/trading/chart',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json, text/plain, */*',
    }

    conn.request(
        'GET',
        f'/trading/1/history?fsk=1770567065937&symbol={symbol_name}&resolution={resolution}&frame=1',
        headers=headers
    )

    response = conn.getresponse()
    return json.loads(response.read().decode())

# Load symbols
symbols = pd.read_csv("stock_symbol_list.csv")['symbol'].tolist()

# Loop through timeframes
for resolution, label in RESOLUTIONS.items():
    timeframe_folder = os.path.join(BASE_FOLDER, resolution)
    os.makedirs(timeframe_folder, exist_ok=True)

    master_csv = os.path.join(timeframe_folder, "all_all_time_stocks.csv")

    # Create master CSV if not exists
    if not os.path.exists(master_csv):
        pd.DataFrame(columns=[
            "Symbol", "Date",
            "Open", "High", "Low", "Close", "Volume"
        ]).to_csv(master_csv, index=False)

    print(f"\n📁 Fetching {label.upper()} data")

    for symbol in symbols:
        try:
            print(f"Fetching {symbol} ({label})...")
            data = fetch_stock_data(symbol, resolution)

            if data.get("s") == "ok" and data.get("t"):
                df = pd.DataFrame({
                    "Symbol": symbol,
                    "Date": pd.to_datetime(data["t"], unit="s"),
                    "Open": data["o"],
                    "High": data["h"],
                    "Low": data["l"],
                    "Close": data["c"],
                    "Volume": data["v"],
                })

                # Save per-symbol CSV
                symbol_csv = os.path.join(timeframe_folder, f"{symbol}.csv")
                df.to_csv(symbol_csv, index=False)

                # Append to timeframe master
                df.to_csv(master_csv, mode="a", header=False, index=False)

                print(f"✅ Saved {symbol} ({label})")

            else:
                print(f"⚠️ No data for {symbol} ({label})")

        except Exception as e:
            print(f"❌ Error {symbol} ({label}): {e}")

print("\n🎉 Done! Daily, Weekly & Monthly masters created.")
