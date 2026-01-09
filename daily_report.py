import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Parameters
SYMBOL = "TSLA"

# Output directory
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Download data
df = yf.download(SYMBOL, period="5d", interval="1d")

# Metrics
open_price = float(df["Open"].iloc[-1])
close_price = float(df["Close"].iloc[-1])
volatility = float(df["Close"].pct_change().std() * 100)

# Date
today = datetime.now().strftime("%Y-%m-%d")

# Report content
report = f"""
DAILY REPORT — {SYMBOL}
Date: {today}

Open price: {open_price:.2f}
Close price: {close_price:.2f}
Volatility: {volatility:.2f} %
"""

# Save report
filename = f"{REPORT_DIR}/report_{today}.txt"
with open(filename, "w") as f:
    f.write(report)

print(f"Report generated: {filename}")

