# Python, Git & Linux Project 

### Author(s)
- Name:Léa NAPASEUTH and Eric MOTHE
- Module: Quantitative Finance – Quant A & Quant B
- Environment: Ubuntu (WSL) + Windows

---

## Project overview

This project consists of building a **complete quantitative finance platform** deployed under Linux.  
The platform is composed of two complementary modules:

- **Quant A**: Single Asset Analysis  
- **Quant B**: Multi-Asset Portfolio Analysis  

Together, these modules simulate a realistic end-to-end quantitative workflow, from market data retrieval to strategy analysis, visualization, and automation.

The project demonstrates practical skills in:
- Python programming for finance,
- Linux-based deployment,
- Git/GitHub version control,
- quantitative strategy implementation,
- portfolio analysis and risk management.

---

## Project architecture

The platform is structured around two independent but coherent components:

###  Quant A – Single Asset Analysis
Focuses on the analysis of a single financial asset (e.g. Tesla – TSLA):
- price analysis,
- quantitative trading strategies,
- performance metrics,
- automated daily reporting.

###  Quant B – Multi-Asset Portfolio Analysis
Extends the analysis to a portfolio of multiple assets:
- diversification and correlation analysis,
- portfolio construction and allocation,
- portfolio-level performance and risk metrics.

---

## Technologies Used:

- **Python 3**
- **Streamlit** (interactive dashboards)
- **yfinance** (historical market data)
- **Finnhub API** (real-time prices)
- **pandas / numpy**
- **scikit-learn** (forecasting – optional bonus)
- **Linux (Ubuntu via WSL)**
- **cron** (task automation)
- **Git / GitHub**

---

## Main Features

### Interactive Dashboards
- Real-time and historical market data visualization
- Strategy and parameter selection via sidebar
- Clear comparison between strategies and assets

### Quantitative Strategies
- Buy & Hold
- Simple Moving Average (SMA)
- Relative Strength Index (RSI)

### Performance Metrics
- Cumulative return
- Maximum drawdown
- Sharpe ratio
- Portfolio volatility and correlations (Quant B)

### Automation
- Daily report generation via a Linux cron job
- Automatic storage of reports and execution logs

---

## Linux Deployment

The entire platform is executed under **Linux using Ubuntu via WSL**, ensuring compatibility with real-world server environments.

