import data_handler as dh
import portfolio as pf
import pandas as pd

df_prices = dh.get_initial_data(dh.symbols)
weights = [0.1]*10
cumulative_value, port_returns = pf.calc_portfolio(df_prices, weights)
metrics = pf.portfolio_metrics(cumulative_value, port_returns)
corr = pf.correlation_matrix(df_prices)

# Sauvegarde CSV
metrics_df = pd.DataFrame([metrics])
metrics_df.to_csv("daily_metrics.csv")
corr.to_csv("daily_correlation.csv")

