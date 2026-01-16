import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Liste de tes 10 actifs
symbols = [
    "AAPL",        
    "^GSPC",       
    "ENGI.PA",    
    "^TNX",        
    "^BUND",       
    "GC=F",        
    "SI=F",        
    "EURUSD=X",    
    "BTC-USD",     
    "ETH-USD"      
]


# Fonction pour récupérer les données historiques
def get_initial_data(symbols, start="2023-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    df_all = pd.DataFrame()

    for sym in symbols:
        try:
            df = yf.download(sym, start=start, end=end)

            # parfois 'Adj Close' n'est pas dispo, on fallback sur 'Close'
            if "Adj Close" in df.columns:
                data = df["Adj Close"]
            else:
                data = df["Close"]

            if not data.empty:
                df_all[sym] = data

        except Exception as e:
            print(f"Erreur pour {sym}: {e}")

    df_all.index.name = "Date"
    return df_all
    
# Fonction pour mettre à jour les données en continu
def update_data(df_prices, symbols):

    if df_prices.empty:
        start = "2020-01-01"
    else:
        last_date = df_prices.index[-1]
        start = last_date + timedelta(days=1)

    end = datetime.today()

    if not df_prices.empty and start >= end:
        return df_prices

    new_data = get_initial_data(
        symbols,
        start=start if isinstance(start, str) else start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d")
    )

    df_prices = pd.concat([df_prices, new_data])
    df_prices = df_prices[~df_prices.index.duplicated(keep="last")]

    return df_prices
