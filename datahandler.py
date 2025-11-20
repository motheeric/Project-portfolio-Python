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
    
# Fonction pour mettre à jour les données en continu
def update_data(df_prices, symbols):
    last_date = df_prices.index[-1]
    start = last_date + timedelta(days=1)
    end = datetime.today()
    if start >= end:
        return df_prices  # rien à mettre à jour
    # Récupérer les nouvelles données
    new_data = get_initial_data(symbols, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    # Concaténer avec les anciennes données et enlever les doublons
    df_prices = pd.concat([df_prices, new_data])
    df_prices = df_prices[~df_prices.index.duplicated(keep='last')]
    return df_prices
