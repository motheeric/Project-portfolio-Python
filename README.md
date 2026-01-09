# Python Git Linux Project – Branch Quant A  


### Owner
- Name: Léa NAPASEUTH
- Branch: Quant A : Single Asset Analysis
- Environment: Ubuntu (WSL) and Windows Powershell

---

## Global overview

This project consists of designing and deploying a professional quantitative finance application under Linux.  
The application allows users to:
- retrieve real-time and historical financial data,
- implement quantitative trading strategies,
- visualize results through an interactive dashboard,
- automate a daily financial report using a cron job.

The project simulates a real-world quantitative finance workflow using Python, Git, and Linux tools.

---

## Technologies used

- **Python 3**
- **Streamlit** (for the interactive dashboard)
- **yfinance** (for the collect of market data)
- **Finnhub API** (real-time prices)
- **pandas / numpy**
- **scikit-learn** (forecasting model – bonus)
- **Linux (Ubuntu via WSL)**
- **cron** (task automation)

---

##  Main features

### Streamlit Dashboard
- Historical price visualization for Tesla (TSLA)
- Real-time price display
- Interactive sidebar (time period, strategy selection, parameter tuning)

### Implemented quantitative strategies
- **Buy & Hold**
- **Simple Moving Average (SMA) Strategy**
- **Relative Strength Index (RSI) Strategy**

### Performance metrics
- Cumulative return
- Maximum drawdown
- Sharpe ratio

### Bonus : Forecasting Model
- Linear regression model (scikit-learn)
- Future price predictions with confidence intervals

---

## Linux deployment

The application is executed under **Linux using Ubuntu via WSL**.

### Running the application:
```bash
source venv/bin/activate
python3 -m streamlit run code.py
Warning : be careful, running only streamlit does not work

### Link dashboard
http://localhost:8501
