import streamlit as st

st.set_page_config(page_title="Portfolio", layout="wide")
choice = st.sidebar.radio("Choisir :", ["Quant A", "Quant B"])

if choice == "Quant A":
    import code.py
else:
    import dashboard.py

