import streamlit as st
import plotly.express as px
import numpy as np
from quantB import data_handler as dh
from quantB import portfolio as pf
import time 

st.title("Dashboard Quant B - Multi-Asset Portfolio")

# Charger les données initiales
df_prices = dh.get_initial_data(dh.symbols)

# Rafraîchissement toutes les 5 minutes
st_autorefresh_interval = 300
last_refresh = st.session_state.get("last_refresh", 0)
if time.time() - last_refresh > st_autorefresh_interval:
    st.session_state.last_refresh = time.time()
    st.rerun() 

# Mise à jour des nouvelles données
df_prices = dh.update_data(df_prices, dh.symbols)

# --- SYNCHRONISATION DES POIDS ET DES ACTIFS ---
available_symbols = df_prices.columns.tolist()

weights = []
st.sidebar.header("Paramètres du portefeuille")

# On boucle sur les colonnes réelles présentes pour éviter l'erreur de "shape mismatch"
for sym in available_symbols:
    w = st.sidebar.slider(f"Poids {sym}", 0.0, 1.0, 0.1)
    weights.append(w)

if len(weights) > 0:
    weights = np.array(weights)
    total_w = weights.sum()
    if total_w > 0:
        weights = weights / total_w
    else:
        weights = np.ones(len(weights)) / len(weights)
else:
    st.error("Aucune donnée disponible pour les symboles sélectionnés.")
    st.stop()

# Calcul du portefeuille
cumulative_value, port_returns = pf.calc_portfolio(df_prices, weights)

if cumulative_value is None:
    st.warning("Pas assez de données pour calculer le portefeuille.")
    st.stop()

metrics = pf.portfolio_metrics(cumulative_value, port_returns)
corr = pf.correlation_matrix(df_prices)

# Graphiques
st.subheader("Valeur cumulée du portefeuille")
fig_portfolio = px.line(cumulative_value, title="Portefeuille cumulatif")
st.plotly_chart(fig_portfolio)

st.subheader("Prix des actifs")
fig_assets = px.line(df_prices, title="Prix des actifs disponibles")
st.plotly_chart(fig_assets)

st.subheader("Matrice de corrélation")
st.dataframe(corr)

st.subheader("KPIs")
st.write(metrics)
