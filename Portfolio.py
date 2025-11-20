import numpy as np
import pandas as pd

# Fonction pour calculer la valeur cumulée et les rendements
def calc_portfolio(df_prices, weights):
    """
    df_prices : DataFrame avec les prix ajustés des 10 actifs
    weights : array ou list des poids (doit sommer à 1)
    """
    # Calcul des rendements journaliers
    returns = df_prices.pct_change().dropna()
    
    # Rendement du portefeuille
    port_returns = returns.dot(weights)
    
    # Valeur cumulée du portefeuille
    cumulative_value = (1 + port_returns).cumprod()
    
    return cumulative_value, port_returns

# Fonction pour calculer les métriques principales
def portfolio_metrics(cumulative_value, port_returns):
    """
    Renvoie un dictionnaire avec les métriques :
    - Mean Return annualisé
    - Volatilité annualisée
    - Sharpe ratio
    - Max drawdown
    """
    mean_ret = port_returns.mean() * 252
    vol = port_returns.std() * np.sqrt(252)
    sharpe = mean_ret / vol
    max_dd = (cumulative_value.cummax() - cumulative_value).max()
    
    return {
        "Mean Return": mean_ret,
        "Volatility": vol,
        "Sharpe": sharpe,
        "Max Drawdown": max_dd
    }

# Fonction pour calculer la corrélation entre les actifs
def correlation_matrix(df_prices):
    returns = df_prices.pct_change().dropna()
    return returns.corr()
