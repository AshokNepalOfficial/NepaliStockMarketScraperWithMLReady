import pandas as pd
import numpy as np

# ===============================
# Technical Indicator Functions
# ===============================

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist


def compute_bbands(series, window=20, num_std=2):
    middle = series.rolling(window).mean()
    std = series.rolling(window).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    width = upper - lower
    return upper, middle, lower, width


def compute_atr(high, low, close, period=14):
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()
    return atr


def compute_adx(high, low, close, period=14):
    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()
    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(period).mean()
    return adx


# ===============================
# Load Data
# ===============================

df = pd.read_csv(
    "all_all_time_stocks_data.csv",
    parse_dates=['Date']
)

df = df.sort_values(
    by=['Symbol', 'Date']
).reset_index(drop=True)

enhanced_data = []

# ===============================
# Feature Engineering
# ===============================

for symbol, group in df.groupby('Symbol'):
    g = group.copy()

    # --- Price-based features ---
    g['return'] = g['Close'].pct_change(fill_method=None)
    g['price_change'] = g['Close'] - g['Open']
    g['high_low_range'] = g['High'] - g['Low']
    g['high_low_pct'] = (g['High'] - g['Low']) / g['Low']
    g['close_open_ratio'] = g['Close'] / g['Open']

    # --- Moving averages ---
    g['SMA_5'] = g['Close'].rolling(5).mean()
    g['SMA_10'] = g['Close'].rolling(10).mean()
    g['EMA_5'] = g['Close'].ewm(span=5, adjust=False).mean()
    g['EMA_10'] = g['Close'].ewm(span=10, adjust=False).mean()

    # --- Volatility / momentum ---
    g['volatility_5'] = g['Close'].rolling(5).std()
    g['momentum_5'] = g['Close'] - g['Close'].shift(5)

    # --- Volume features ---
    g['vol_change'] = g['Volume'].pct_change(fill_method=None)
    g['avg_volume_5'] = g['Volume'].rolling(5).mean()

    # --- Technical indicators ---
    g['rsi_14'] = compute_rsi(g['Close'])

    g['macd'], g['macd_signal'], g['macd_hist'] = compute_macd(g['Close'])

    g['bb_upper'], g['bb_middle'], g['bb_lower'], g['bb_width'] = compute_bbands(g['Close'])

    g['ATR_14'] = compute_atr(g['High'], g['Low'], g['Close'])

    g['ADX_14'] = compute_adx(g['High'], g['Low'], g['Close'])

    # --- EMA cross ---
    g['ema_cross'] = 0
    g.loc[g['EMA_5'] > g['EMA_10'], 'ema_cross'] = 1
    g.loc[g['EMA_5'] < g['EMA_10'], 'ema_cross'] = -1

    # --- Time features ---
    g['day_of_week'] = g['Date'].dt.dayofweek
    g['month'] = g['Date'].dt.month

    # --- Lag features ---
    for lag in [1, 2, 3]:
        g[f'return_lag_{lag}'] = g['return'].shift(lag)
        g[f'vol_change_lag_{lag}'] = g['vol_change'].shift(lag)
        g[f'rsi_14_lag_{lag}'] = g['rsi_14'].shift(lag)
        g[f'macd_lag_{lag}'] = g['macd'].shift(lag)
        g[f'ema_cross_lag_{lag}'] = g['ema_cross'].shift(lag)
        g[f'ATR_14_lag_{lag}'] = g['ATR_14'].shift(lag)
        g[f'ADX_14_lag_{lag}'] = g['ADX_14'].shift(lag)
        g[f'bb_width_lag_{lag}'] = g['bb_width'].shift(lag)

    # --- Targets ---
    g['next_day_return'] = g['Close'].shift(-1) / g['Close'] - 1
    g['direction'] = (g['next_day_return'] > 0).astype(int)

    enhanced_data.append(g)

# ===============================
# Final Dataset
# ===============================

final_df = pd.concat(enhanced_data, ignore_index=True)
final_df = final_df.dropna().reset_index(drop=True)

final_df.to_csv(
    "all_stocks_data_ml_ready_new.csv",
    index=False
)

print("✅ ML-ready dataset saved to all_stocks_data_ml_ready_new.csv")
