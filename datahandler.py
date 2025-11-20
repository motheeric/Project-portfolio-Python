import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Liste de tes 10 actifs
symbols = ["AAPL","SP500","ENGI","US10Y","Bund10Y","XAUUSD","XAGUSD","EURUSD","BTCUSD","ETHUSD"]

# Fonction pour récupérer les données historiques
def get_initial_data(symbols, start="2023-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")
    df_all = pd.DataFrame()
    for sym in symbols:
        try:
            data = yf.download(sym, start=start, end=end)['Adj Close']
            df_all[sym] = data
        except Exception as e:
            print(f"Erreur pour {sym}: {e}")
    df_all.index.name = 'Date'
    return df_all
