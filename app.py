import streamlit as st
import runpy
from pathlib import Path

st.set_page_config(page_title="Portfolio", layout="wide")

BASE = Path(__file__).resolve().parent

choice = st.sidebar.radio("Choisir :", ["Quant A", "Quant B"])

if choice == "Quant A":
    runpy.run_path(str(BASE / "quant A" / "code.py"), run_name="__main__")
else:
    runpy.run_path(str(BASE / "quant B" / "dashboard.py"), run_name="__main__")
