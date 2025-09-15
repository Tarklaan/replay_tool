import streamlit as st
from utils.exchange_utils import get_metatrader_symbols, download_symbol_history
from utils.chart import plot_candles
from data.data_loader import load_data # if you need any

st.title("Replay Tool")

# Step 1: Get symbols
if st.button("Load Instruments"):
    symbols = get_metatrader_symbols()
    st.session_state["symbols"] = symbols
    st.success(f"Loaded {len(symbols)} instruments")

# Step 2: Select one instrument
if "symbols" in st.session_state:
    symbol = st.selectbox("Select a symbol", st.session_state["symbols"])

    if st.button("Download History (2021 → now)"):
        df = download_symbol_history(symbol)
        if df is not None:
            st.success(f"Downloaded {len(df)} rows for {symbol}")

    if st.button("Load from DB"):
        df = load_candles(symbol, limit=1000)
        st.write(df.head())
