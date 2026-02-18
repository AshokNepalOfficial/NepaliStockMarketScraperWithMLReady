import http.client
import json
import pandas as pd
import os
import random
import time

BASE_HOST = "nepsealpha.com"
BASE_FOLDER = "stock_data"

RESOLUTIONS = {
    "1": "full_day",
    "1D": "daily",
}

os.makedirs(BASE_FOLDER, exist_ok=True)


# =========================================================
# COOKIE HANDLING
# =========================================================
def extract_cookies(headers):
    cookies = []
    for k, v in headers:
        if k.lower() == "set-cookie":
            cookies.append(v.split(";", 1)[0])
    return "; ".join(cookies)


# =========================================================
# CREATE SESSION (VISIT HOME)
# =========================================================
def create_session():
    conn = http.client.HTTPSConnection(BASE_HOST, timeout=10)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1 Edg/145.0.0.0'
    }

    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()

    cookies = extract_cookies(res.getheaders())
    res.read()  # consume body

    if not cookies:
        raise Exception("❌ Failed to obtain session cookies")
    return cookies



# =========================================================
# GET FSK TOKEN
# =========================================================
def get_fsk(cookies):
    conn = http.client.HTTPSConnection(BASE_HOST, timeout=120)
    fs = f"0.{random.randint(10_000_000, 99_999_999)}"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1 Edg/145.0.0.0',
        'cookie': f'{cookies}',
    }


    conn.request("GET", f"/force-url-key?fs=0.{fs}", headers=headers)
    res = conn.getresponse()

    data = json.loads(res.read().decode())
    # print(data)

    if "key" not in data:
        raise Exception("❌ FSK not found")
    # print(data["key"])
    return data["key"]


# =========================================================
# FETCH HISTORICAL DATA
# =========================================================
def fetch_history(symbol, resolution, fsk, cookies):
    # print(resolution)
    conn = http.client.HTTPSConnection('nepsealpha.com')
    headers = {
        'Referer': 'https://nepsealpha.com/trading/chart',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1 Edg/145.0.0.0',
        'Accept': 'application/json, text/plain, */*',
    }
    conn.request(
        'GET',
        f'/trading/1/history?fsk={fsk}&symbol={symbol}&resolution={resolution}',
        headers=headers
    )
    res = conn.getresponse()

    if res.status != 200:
        raise Exception(f"HTTP {res.status}")

    return json.loads(res.read().decode())


# =========================================================
# MAIN
# =========================================================
def main():
    symbols = pd.read_csv("stock_symbol_list.csv")["symbol"].tolist()

    cookies = create_session()

    for resolution, label in RESOLUTIONS.items():
        print(f"\n📁 Processing {label.upper()}")

        folder = os.path.join(BASE_FOLDER, label)
        os.makedirs(folder, exist_ok=True)

        master_csv = os.path.join(folder, "all_all_time_stocks.csv")

        if not os.path.exists(master_csv):
            pd.DataFrame(columns=[
                "Symbol", "Date", "Open",
                "High", "Low", "Close", "Volume"
            ]).to_csv(master_csv, index=False)

        fsk = get_fsk(cookies)

        for symbol in symbols:
            retries = 2

            while retries > 0:
                try:
                    print(f"Fetching {symbol}...")

                    data = fetch_history(symbol, resolution, fsk, cookies)

                    if data.get("s") != "ok":
                        print("🔄 Refreshing token...")
                        cookies = create_session()
                        fsk = get_fsk(cookies)
                        retries -= 1
                        continue

                    if not data.get("t"):
                        print(f"⚠️ No data for {symbol}")
                        break

                    df = pd.DataFrame({
                        "Symbol": symbol,
                        "Date": pd.to_datetime(data["t"], unit="s"),
                        "Open": data["o"],
                        "High": data["h"],
                        "Low": data["l"],
                        "Close": data["c"],
                        "Volume": data["v"],
                    })

                    df.to_csv(os.path.join(folder, f"{symbol}.csv"), index=False)
                    df.to_csv(master_csv, mode="a", header=False, index=False)

                    print(f"✅ Saved {symbol}")
                    break

                except Exception as e:
                    print(f"❌ Error {symbol}: {e}")
                    retries -= 1
                    time.sleep(1)

        print(f"✅ Completed {label}")

    print("\n🎉 ALL DONE!")


if __name__ == "__main__":
    main()
