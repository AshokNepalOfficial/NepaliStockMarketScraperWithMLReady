# 📈 NepaliStockMarketScraperWithMLReady

A complete end-to-end data pipeline for collecting, processing, and preparing **Nepali stock market data** for **Machine Learning and Quantitative Analysis**.

This project:

* ✅ Scrapes historical OHLCV data
* ✅ Organizes multi-timeframe datasets
* ✅ Generates master datasets
* ✅ Engineers advanced technical indicators
* ✅ Produces an ML-ready dataset

Built specifically for working with data from the **Nepal Stock Exchange (NEPSE)** via publicly available endpoints such as **NepseAlpha**.

---

# 🚀 Project Overview

NepaliStockMarketScraperWithMLReady is designed for:

* 📊 Data Scientists
* 🤖 Machine Learning Engineers
* 📈 Quantitative Traders
* 🎓 Academic Researchers
* 🧠 Financial Model Builders

It provides a **clean, structured, and feature-rich dataset** ready for:

* Classification (Up / Down prediction)
* Regression (Return prediction)
* Time-series forecasting
* Deep learning models (LSTM, Transformers)
* Reinforcement learning strategies

---

# 🗂 Project Structure

```
NepaliStockMarketScraperWithMLReady/
│
├── stock_symbol_list.csv
├── stock_scraper.py
├── extracolumn.py
├── stock_data/
│   ├── 1/
│   └── 1D/
│
├── all_all_time_stocks.csv
├── all_stocks_data_ml_ready_new.csv
└── README.md
```

---

# 🔍 Data Pipeline Flow

### Step 1️⃣ – Fetch Historical Data

* Pulls OHLCV data per symbol
* Supports multiple resolutions:

  * `"1"` → Full Day
  * `"1D"` → Daily

### Step 2️⃣ – Save Structured Data

For each timeframe:

* Individual CSV per stock
* One master CSV combining all stocks

### Step 3️⃣ – Feature Engineering

Adds:

* Technical indicators
* Momentum features
* Volatility features
* Lag variables
* ML target columns

### Step 4️⃣ – Export ML-Ready Dataset

Final cleaned dataset:

```
all_stocks_data_ml_ready_new.csv
```

---

# ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ashoknepalofficial/NepaliStockMarketScraperWithMLReady.git
cd NepaliStockMarketScraperWithMLReady
```

### 2️⃣ Install Dependencies

```bash
pip install pandas numpy
```

Python 3.8+ recommended.

---

# 🧾 Step 1 – Stock Data Scraper

The scraper:

* Connects to Nepali stock API endpoint
* Fetches OHLCV data
* Saves:

  * Per-stock CSV
  * Master CSV

### Base Configuration

```python
BASE_FOLDER = "stock_data"

RESOLUTIONS = {
    "1": "full_day",
    "1D": "daily",
}
```

### Output Structure

```
stock_data/
   ├── 1/
   │     ├── NABIL.csv
   │     ├── SCB.csv
   │     └── all_all_time_stocks.csv
   │
   └── 1D/
         ├── NABIL.csv
         ├── SCB.csv
         └── all_all_time_stocks.csv
```

---

# 🧠 Step 2 – Feature Engineering (ML Ready)

`extracolumn.py` transforms raw OHLCV into advanced ML features.

---

# 📊 Engineered Features

## 🔹 Basic Market Data

* Symbol
* Date
* Open
* High
* Low
* Close
* Volume

---

## 🔹 Price-Based Features

* `return`
* `price_change`
* `high_low_range`
* `high_low_pct`
* `close_open_ratio`

---

## 🔹 Moving Averages

* `SMA_5`
* `SMA_10`
* `EMA_5`
* `EMA_10`

---

## 🔹 Volatility & Momentum

* `volatility_5`
* `momentum_5`
* `vol_change`
* `avg_volume_5`

---

## 🔹 Technical Indicators

### RSI (14)

Relative Strength Index

### MACD

* macd
* macd_signal
* macd_hist

### Bollinger Bands

* bb_upper
* bb_middle
* bb_lower
* bb_width

### ATR (14)

Average True Range

### ADX (14)

Average Directional Index

### EMA Cross

* 1 → Bullish crossover
* -1 → Bearish crossover

---

## 🔹 Time-Based Features

* day_of_week (0–6)
* month (1–12)

---

## 🔹 Lag Features (1–3 days)

For:

* returns
* volume changes
* RSI
* MACD
* EMA cross
* ATR
* ADX
* Bollinger width

---

## 🎯 Target Variables

* `next_day_return`
* `direction` (1 = Up, 0 = Down)

Perfect for supervised learning.

---

# 🏁 Final Output

After feature engineering:

```
all_stocks_data_ml_ready_new.csv
```

* Cleaned
* Sorted
* NaN removed
* Fully ML-ready

---

# 💻 Example Usage

## Load Dataset

```python
import pandas as pd

df = pd.read_csv("all_stocks_data_ml_ready_new.csv")
print(df.head())
```

## Train Classification Model

```python
X = df.drop(columns=["direction", "next_day_return", "Symbol", "Date"])
y = df["direction"]
```

---

# 📈 Example Use Cases

* 📊 Next-day price prediction
* 📉 Volatility modeling
* 🤖 LSTM stock forecasting
* 🧠 Feature importance analysis
* 💹 Algorithmic trading backtesting
* 🔁 Reinforcement learning agents

---

# 🛠 Customization

You can easily:

* Add new indicators (Stochastic, OBV, CCI, etc.)
* Increase lag windows
* Add multi-timeframe merging
* Add fundamental data
* Implement real-time streaming

---

# ⚠️ Disclaimer

This project is for:

* Educational use
* Research
* Non-commercial experimentation

It is **NOT financial advice**.

Trading stocks involves risk. Always conduct your own research before investing.

---

# 📜 License

This project is released under:

**CC-BY-SA-4.0**

You are free to:

* Share
* Adapt
* Modify

With proper attribution.

---

# 👨‍💻 Author

Developed for quantitative research on the Nepali stock market.

If you found this useful:

⭐ Star the repo
🍴 Fork it
📢 Share it

---

# 🚀 Future Improvements

* Deep learning examples
* Model benchmarking
* AutoML integration
* API-based live updates
* Dockerized deployment
* Cloud storage integration

---

# 🎉 Final Note

NepaliStockMarketScraperWithMLReady provides one of the most complete **Nepali stock ML datasets** publicly available — from raw scraping to ML-ready features.

Happy Modeling! 📊🤖
