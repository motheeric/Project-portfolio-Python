import streamlit as st
import runpy
from pathlib import Path

st.set_page_config(page_title="Portfolio", layout="wide")

BASE = Path(__file__).resolve().parent

choice = st.sidebar.radio("Choisir :", ["QuantA", "QuantB"])

if choice == "QuantA":
    runpy.run_path(str(BASE / "quantA" / "code.py"), run_name="__main__")
else:
    runpy.run_path(str(BASE / "quantB" / "dashboard.py"), run_name="__main__")
