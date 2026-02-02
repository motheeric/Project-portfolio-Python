import numpy as np
import pandas as pd

# returns calculation
def calc_portfolio(df_prices, weights):
    if df_prices is None or df_prices.empty or len(df_prices) < 2:
        return None, None

    returns = df_prices.pct_change()

    if returns.dropna().empty:
        return None, None

    returns = returns.dropna()

    port_returns = returns.dot(weights)
    cumulative_value = (1 + port_returns).cumprod()

    return cumulative_value, port_returns


# metrics
def portfolio_metrics(cumulative_value, port_returns):

    if cumulative_value is None or port_returns is None or port_returns.empty:
        return None

    mean_ret = port_returns.mean() * 252
    vol = port_returns.std() * np.sqrt(252)
    sharpe = mean_ret / vol if vol != 0 else np.nan
    max_dd = (cumulative_value.cummax() - cumulative_value).max()

    return {
        "Mean Return": mean_ret,
        "Volatility": vol,
        "Sharpe": sharpe,
        "Max Drawdown": max_dd
    }


# correlation
def correlation_matrix(df_prices):
    if df_prices is None or df_prices.empty or len(df_prices) < 2:
        return None

    returns = df_prices.pct_change().dropna()

    if returns.empty:
        return None

    return returns.corr()
