import streamlit as st
import plotly.express as px
import numpy as np
import data_handler as dh
import portfolio as pf
from streamlit_autorefresh import st_autorefresh

st.title("Dashboard Quant B - Multi-Asset Portfolio")

# Charger les données initiales
df_prices = dh.get_initial_data(dh.symbols)

# Rafraîchissement toutes les 5 minutes
st_autorefresh(interval=300000, key="refresh")

# Mise à jour des nouvelles données
df_prices = dh.update_data(df_prices, dh.symbols)

# Curseurs pour modifier les poids
weights = []
st.sidebar.header("Paramètres du portefeuille")
for sym in dh.symbols:
    w = st.sidebar.slider(f"Poids {sym}", 0.0, 1.0, 0.1)
    weights.append(w)
weights = np.array(weights)
weights = weights / weights.sum()  # normaliser pour que la somme = 1

# Calcul du portefeuille
cumulative_value, port_returns = pf.calc_portfolio(df_prices, weights)
metrics = pf.portfolio_metrics(cumulative_value, port_returns)
corr = pf.correlation_matrix(df_prices)

# Graphiques
st.subheader("Valeur cumulée du portefeuille")
fig_portfolio = px.line(cumulative_value, title="Portefeuille cumulatif")
st.plotly_chart(fig_portfolio)

st.subheader("Prix des actifs")
fig_assets = px.line(df_prices, title="Prix des 10 actifs")
st.plotly_chart(fig_assets)

st.subheader("Matrice de corrélation")
st.dataframe(corr)

st.subheader("KPIs")
st.write(metrics)

