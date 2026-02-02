import streamlit as st
import plotly.express as px
import numpy as np
from quantB import data_handler as dh
from quantB import portfolio as pf
import time 

st.title("Dashboard Quant B - Multi-Asset Portfolio")

# Loading initial data
df_prices = dh.get_initial_data(dh.symbols)

# Refresh every 5min
st_autorefresh_interval = 300
last_refresh = st.session_state.get("last_refresh", 0)
if time.time() - last_refresh > st_autorefresh_interval:
    st.session_state.last_refresh = time.time()
    st.rerun() 

# update the data
df_prices = dh.update_data(df_prices, dh.symbols)

# synchronize weights 
available_symbols = df_prices.columns.tolist()

weights = []
st.sidebar.header("Paramètres du portefeuille")

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
    st.error("No available data")
    st.stop()

# Portfolio calculations
cumulative_value, port_returns = pf.calc_portfolio(df_prices, weights)

if cumulative_value is None:
    st.warning("not enough data.")
    st.stop()

metrics = pf.portfolio_metrics(cumulative_value, port_returns)
corr = pf.correlation_matrix(df_prices)

# Graphics
st.subheader("cumulative value of the portfolio")
fig_portfolio = px.line(cumulative_value, title="Portfolio value")
st.plotly_chart(fig_portfolio)

st.subheader("assets prices")
fig_assets = px.line(df_prices, title="assets prices ")
st.plotly_chart(fig_assets)

st.subheader("correlation matrice")
st.dataframe(corr)

st.subheader("KPIs")
st.write(metrics)
