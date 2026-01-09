# Python Git Linux Project – Branch Quant A  


### 👤 Author
- Name: Léa NAPASEUTH
- Branch: Quant A : Single Asset Analysis
- Environment: Ubuntu (WSL) and Windows Powershell

---

## 📌 Project Overview

This project consists of designing and deploying a professional quantitative finance application under Linux.  
The application allows users to:
- retrieve real-time and historical financial data,
- implement quantitative trading strategies,
- visualize results through an interactive dashboard,
- automate a daily financial report using a cron job.

The project simulates a real-world quantitative finance workflow using Python, Git, and Linux tools.

---

## 🛠️ Technologies Used

- **Python 3**
- **Streamlit** (for the interactive dashboard)
- **yfinance** (for the collect of market data)
- **Finnhub API** (real-time prices)
- **pandas / numpy**
- **scikit-learn** (forecasting model – bonus)
- **Linux (Ubuntu via WSL)**
- **cron** (task automation)

---

## 📊 Main Features

### 🔹 Streamlit Dashboard
- Historical price visualization for Tesla (TSLA)
- Real-time price display
- Interactive sidebar (time period, strategy selection, parameter tuning)

### 🔹 Implemented Quantitative Strategies
- **Buy & Hold**
- **Simple Moving Average (SMA) Strategy**
- **Relative Strength Index (RSI) Strategy**

### 🔹 Performance Metrics
- Cumulative return
- Maximum drawdown
- Sharpe ratio

### 🔹 Bonus – Forecasting Model
- Linear regression model (scikit-learn)
- Future price predictions with confidence intervals

---

## 🐧 Linux Deployment

The application is executed under **Linux using Ubuntu via WSL**.

### Running the application:
```bash
source venv/bin/activate
python3 -m streamlit run app1.py
Warning : be careful, running only streamlit does not work
