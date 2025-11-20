# Dashboard Streamlit - Code Python pour Quant A

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
# STRATEGIE MOMENTUM MA10
# --------------------------
st.subheader("Stratégie Momentum (MA10)")

# Vérifier que la colonne Close existe
if "Close" not in df.columns:
    st.error("Les données Yahoo Finance ne contiennent pas de colonne 'Close'.")
else:
    # Calcul MA10
    df["MA10"] = df["Close"].rolling(window=10).mean()

    # Vérifier que MA10 est bien créée
    if "MA10" not in df.columns:
        st.error("Erreur : la colonne MA10 n'a pas pu être créée.")
    else:
        # Filtrer les données valides
        df_mom = df.dropna(subset=["MA10"]).copy()

        if df_mom.empty:
            st.error("Pas assez de données pour calculer MA10 (min 10 jours).")
        else:
            # Calcul momentum
            df_mom["Signal"] = (df_mom["Close"] > df_mom["MA10"]).astype(int)
            df_mom["Return"] = df_mom["Close"].pct_change()
            df_mom["Strategy_Return"] = df_mom["Return"] * df_mom["Signal"].shift(1)

            # Performance
            mom_return = df_mom["Strategy_Return"].sum() * 100

            st.metric("Rendement Momentum MA10", f"{mom_return:.2f}%")

