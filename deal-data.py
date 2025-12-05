import pandas as pd
import yfinance as yf

TICKERS = ["COF"]
START_DATE = "2024-02-01"
END_DATE = "2025-06-30"

data = yf.download(
    TICKERS,
    start=START_DATE,
    end=END_DATE,
    auto_adjust=True,
    progress=False,
    group_by="ticker"
)

close_cols = []
for tk in TICKERS:
    close_cols.append(data[tk]["Close"].rename(tk))

prices = pd.concat(close_cols, axis=1).dropna(how="all")
prices = prices.loc["2024-02-04":"2025-06-18"]

prices.index.name = "Date"
output_file = "COF_prices_2024-02-04_2025-06-18.csv"
prices.to_csv(output_file, sep=";")

print("File created:", output_file)
print(prices.head())
print(prices.tail())
