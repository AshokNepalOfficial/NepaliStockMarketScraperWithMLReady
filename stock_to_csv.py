import json
import pandas as pd

# Load JSON file
with open("stock.json", "r") as f:
    data = json.load(f)

# 'value' contains the list of stock dictionaries
stocks = data['value']

# Convert list of dicts to DataFrame
df = pd.DataFrame(stocks)

# Optional: if you want to join lists into a string
df['logo_urls'] = df['logo_urls'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
df['exchange_logo'] = df['exchange_logo'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

# Save to CSV
df.to_csv("stocks.csv", index=False)

print("Saved to stocks.csv")
