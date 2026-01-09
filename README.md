# Python, Git & Linux Project – Quant B  

### Owner
- Name: Eric Mothe
- Module: Quant B – Multi-Asset Portfolio Analysis
- Environment: Ubuntu (WSL) + Windows

---

## Project overview

This project extends the quantitative finance platform developed in Quant A by introducing **multi-asset portfolio analysis** under Linux.  
The objective is to design a professional portfolio dashboard capable of handling multiple assets simultaneously and simulating portfolio-level strategies.

The application allows users to:
- retrieve real-time and historical data for several assets,
- build and simulate portfolios with different allocation rules,
- analyze diversification and correlation effects,
- visualize portfolio performance and risk metrics interactively.

The project follows a realistic quantitative finance workflow using Python, Git, and Linux.

---

## Technologies used

- **Python 3**
- **Streamlit** (interactive dashboard)
- **yfinance** (multi-asset market data)
- **pandas / numpy**
- **scikit-learn** (optional ML extensions)
- **Linux (Ubuntu via WSL)**
- **Git / GitHub** (collaboration and version control)

---

## Main features

### Multi-Asset data handling
- Simultaneous retrieval of historical price data for **at least three assets**
- Automatic data alignment and cleaning
- User-selected asset universe

### Portfolio construction
- **Equal-weight portfolio**
- **Custom-weight portfolio** defined by the user
- Portfolio rebalancing based on user-defined parameters

### Portfolio performance metrics
- Portfolio cumulative return
- Portfolio volatility
- Correlation matrix between assets
- Diversification effects compared to single assets

### Interactive dashboard
- Asset and portfolio selection via sidebar
- Adjustable portfolio weights and parameters
- Clear visual comparison between:
  - individual asset performance
  - aggregated portfolio performance

---

## Visualizations

- Time series of **multiple asset prices**
- Cumulative portfolio value over time
- Correlation heatmap
- Comparison plots: single asset vs portfolio

The main chart displays:
- individual asset price evolutions
- portfolio cumulative value on the same figure

---

## Linux Deployment

The application is executed under **Linux using Ubuntu via WSL**, ensuring compatibility with server-side deployment.

### Running the application:
```bash
source venv/bin/activate
python3 -m streamlit run dashboard.py

