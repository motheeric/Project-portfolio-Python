import streamlit as st
import requests
import os
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression   


# Max drawdown and sharpe ratio

def max_drawdown(cumulative_returns):
    cumulative_returns = pd.Series(cumulative_returns).ravel()
    running_max = pd.Series(cumulative_returns).cummax()
    dd = (cumulative_returns - running_max) / running_max
    return dd.min() * 100

def sharpe_ratio(returns, risk_free_rate=0.0):
    returns = pd.Series(returns).astype(float)
    excess = returns - risk_free_rate

    if excess.std() == 0 or pd.isna(excess).all():
        return 0

    return (excess.mean() / excess.std()) * np.sqrt(252)


# prediction model

def linear_regression_forecast(df, horizon=7):
    """
    Future forecasts using sklearn LinearRegression.
    Returns a clean 1D vector for Pandas.
    """

    df = df.copy()
    df["t"] = np.arange(len(df))
    X = df["t"].values.reshape(-1, 1)
    y = df["Close"].values

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    predictions = model.predict(future_t)

    return predictions.ravel()


# confidence interval

def confidence_intervals(df, predictions):
    """
    Simple confidence interval based on residual variance.
    CI = prediction ± 1 residual standard deviation
    """

    y = df["Close"].values
    t = np.arange(len(df)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(t, y)

    residuals = y - model.predict(t)
    sigma = residuals.std()

    upper = predictions + sigma
    lower = predictions - sigma

    return upper, lower


# finnhub price

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_current_price(symbol="TSLA"):
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": FINNHUB_API_KEY}
    response = requests.get(url, params=params).json()
    return response


# Sidebar interactivity

st.sidebar.header("Parameters")

period_choice = st.sidebar.selectbox(
    "Data period",
    ["6mo", "1y", "2y", "5y"],
    index=2
)

strategy_choice = st.sidebar.selectbox(
    "Strategy",
    ["Buy & Hold", "SMA", "RSI"],
    index=0
)

sma_fast = st.sidebar.number_input("Short-term SMA", 5, 200, 50)
sma_slow = st.sidebar.number_input("Long-term SMA", 20, 500, 200)

rsi_period = st.sidebar.slider("RSI period", 5, 30, 14)
rsi_buy = st.sidebar.slider("RSI buy threshold", 5, 50, 30)
rsi_sell = st.sidebar.slider("RSI sell threshold", 50, 95, 70)


# Historical data

def get_historical_data(symbol="TSLA", period="2y"):
    df = yf.download(symbol, period=period, interval="1d")
    return df.dropna()

df = get_historical_data(period=period_choice)


# Display price

st.title("Quant A — Tesla Dashboard")

price = get_current_price()
if "c" in price:
    st.metric("Current price", price["c"], delta=price.get("d", 0))


st.subheader("Historical price chart")
st.line_chart(df["Close"])


# Prediction and confidence interval

st.subheader("Price forecast (Linear Regression with Confidence Interval)")

horizon = st.slider("Forecast horizon (days)", 3, 30, 7)

pred = linear_regression_forecast(df, horizon=horizon)
upper, lower = confidence_intervals(df, pred)

future_dates = pd.date_range(start=df.index[-1], periods=horizon + 1, freq="D")[1:]

df_pred = pd.DataFrame({
    "Forecast": pred,
    "Upper bound": upper,
    "Lower bound": lower
}, index=future_dates)

combined_pred = pd.concat([df["Close"], df_pred], axis=1)

st.line_chart(combined_pred)


# Buy & Hold

if strategy_choice == "Buy & Hold":

    st.subheader("Buy & Hold strategy")

    price_norm = (df["Close"] / df["Close"].iloc[0]).values.ravel()
    df["BH_Cumulative"] = price_norm

    bh_return = (df["BH_Cumulative"][-1] - 1) * 100
    bh_mdd = max_drawdown(df["BH_Cumulative"])
    bh_sharpe = sharpe_ratio(df["BH_Cumulative"].tolist()[1:])

    st.metric("Total return", f"{bh_return:.2f}%")
    st.metric("Max drawdown", f"{bh_mdd:.2f}%")
    st.metric("Sharpe ratio", f"{bh_sharpe:.2f}")

    st.subheader("Price vs Buy & Hold")

    combined = pd.DataFrame({
        "Normalized price": price_norm,
        "Buy & Hold value": df["BH_Cumulative"].values.ravel()
    }, index=df.index)

    st.line_chart(combined)


# SMA strategy

if strategy_choice == "SMA":

    st.subheader("SMA strategy")

    df["SMA_Fast"] = df["Close"].rolling(sma_fast).mean()
    df["SMA_Slow"] = df["Close"].rolling(sma_slow).mean()
    df_sma = df.dropna().copy()

    if len(df_sma) == 0:
        st.error("Time period too short for SMA.")
    else:
        df_sma["Signal"] = (df_sma["SMA_Fast"] > df_sma["SMA_Slow"]).astype(int)
        df_sma["Return"] = df_sma["Close"].pct_change()
        df_sma["Strategy_Return"] = df_sma["Return"] * df_sma["Signal"].shift(1)
        df_sma["Cumulative"] = (1 + df_sma["Strategy_Return"]).cumprod()

        sma_return = (df_sma["Cumulative"].iloc[-1] - 1) * 100
        sma_mdd = max_drawdown(df_sma["Cumulative"])
        sma_sharpe = sharpe_ratio(df_sma["Strategy_Return"])

        st.metric("Total return", f"{sma_return:.2f}%")
        st.metric("Max drawdown", f"{sma_mdd:.2f}%")
        st.metric("Sharpe ratio", f"{sma_sharpe:.2f}")

        combined = pd.DataFrame({
            "Normalized price": (df_sma["Close"] / df_sma["Close"].iloc[0]).values.ravel(),
            "SMA strategy value": df_sma["Cumulative"].values.ravel()
        }, index=df_sma.index)

        st.line_chart(combined)


# RSI strategy

if strategy_choice == "RSI":

    st.subheader("RSI strategy")

    def compute_RSI(series, period=14):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        return 100 - (100 / (1 + rs))

    df["RSI"] = compute_RSI(df["Close"], rsi_period)
    df_rsi = df.dropna().copy()

    df_rsi["Signal"] = 0
    df_rsi.loc[df_rsi["RSI"] < rsi_buy, "Signal"] = 1
    df_rsi.loc[df_rsi["RSI"] > rsi_sell, "Signal"] = 0
    df_rsi["Signal"] = df_rsi["Signal"].shift(1).fillna(0)

    df_rsi["Return"] = df_rsi["Close"].pct_change()
    df_rsi["Strategy_Return"] = df_rsi["Return"] * df_rsi["Signal"]
    df_rsi["Cumulative"] = (1 + df_rsi["Strategy_Return"]).cumprod()

    rsi_return = (df_rsi["Cumulative"].iloc[-1] - 1) * 100
    rsi_mdd = max_drawdown(df_rsi["Cumulative"])
    rsi_sharpe = sharpe_ratio(df_rsi["Strategy_Return"])

    st.metric("Total return", f"{rsi_return:.2f}%")
    st.metric("Max drawdown", f"{rsi_mdd:.2f}%")
    st.metric("Sharpe ratio", f"{rsi_sharpe:.2f}")

    combined_rsi = pd.DataFrame({
        "Normalized price": (df_rsi["Close"] / df_rsi["Close"].iloc[0]).values.ravel(),
        "RSI strategy value": df_rsi["Cumulative"].values.ravel()
    }, index=df_rsi.index)

    st.line_chart(combined_rsi)
