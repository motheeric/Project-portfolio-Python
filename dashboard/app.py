import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

# --------------------------
# PRIX ACTUEL (FINNHUB)
# --------------------------

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_current_price(symbol="TSLA"):
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": FINNHUB_API_KEY}
    response = requests.get(url, params=params).json()
    return response


# --------------------------
# HISTORIQUE (YAHOO FINANCE)
# --------------------------

def get_historical_data(symbol="TSLA"):
    df = yf.download(symbol, period="6mo", interval="1d")
    df = df.dropna()
    return df


# --------------------------
# DASHBOARD
# --------------------------

st.title("Quant A - Tesla Dashboard")

# Prix actuel
data = get_current_price()
if "c" in data:
    st.metric("Prix actuel (USD)", data["c"], delta=data.get("d", 0))
else:
    st.error("Erreur Finnhub - prix non récupéré")

# Historique
st.subheader("Historique des prix de TSLA")

df = get_historical_data()

if df is not None and not df.empty:

    # --- Graphique prix ---
    st.line_chart(df["Close"])

    # --------------------------
    # STRATEGIE BUY & HOLD
    # --------------------------
    st.subheader("Stratégie Buy & Hold (6 mois)")

    start_price = df["Close"].iloc[0].item()
    end_price = df["Close"].iloc[-1].item()

    bh_return = (end_price / start_price - 1) * 100
    st.metric("Rendement Buy & Hold", f"{bh_return:.2f}%")

    # --------------------------
    # STRATEGIE SMA50 / SMA200
    # --------------------------
    st.subheader("Stratégie SMA50 / SMA200 (Golden Cross - Death Cross)")

    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()

    df_sma = df.dropna().copy()

    if df_sma.empty:
        st.error("Pas assez de données pour SMA50/SMA200 (min 200 jours).")
    else:
        # Signal : 1 = investis, 0 = hors marché
        df_sma["Signal"] = (df_sma["SMA50"] > df_sma["SMA200"]).astype(int)

        # Rendements
        df_sma["Return"] = df_sma["Close"].pct_change()

        # Stratégie (signal décalé de 1 jour)
        df_sma["Strategy_Return"] = df_sma["Return"] * df_sma["Signal"].shift(1)

        # Performance cumulée
        df_sma["Cumulative"] = (1 + df_sma["Strategy_Return"]).cumprod()

        # Performance finale
        sma_return = (df_sma["Cumulative"].iloc[-1] - 1) * 100
        st.metric("Rendement SMA50/SMA200", f"{sma_return:.2f}%")

        # Graphique comparatif
        st.subheader("Comparaison : Prix vs Stratégie SMA")

        combined = pd.DataFrame({
            "Prix normalisé": df_sma["Close"] / df_sma["Close"].iloc[0],
            "Stratégie SMA50/SMA200": df_sma["Cumulative"]
        })

        st.line_chart(combined)

else:
    st.error("Erreur chargement des données Yahoo Finance.")
