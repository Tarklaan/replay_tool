import streamlit as st

# Internal imports (match project structure)
from replay_tool.utils.exchange_utils import get_metatrader_symbols, download_symbol_history
from replay_tool.ui.chart import plot_candles
from replay_tool.utils.utils_db import load_candles


# --- Streamlit UI ---
st.set_page_config(page_title="Replay Tool", layout="wide")
st.title("📈 Trading Replay Tool")


# Step 1: Load Instruments
if st.button("🔄 Load Instruments"):
    symbols = get_metatrader_symbols()
    st.session_state["symbols"] = symbols
    st.success(f"Loaded {len(symbols)} instruments ✅")


# Step 2: Symbol selection
if "symbols" in st.session_state:
    symbol = st.selectbox("🎯 Select a symbol", st.session_state["symbols"])

    # Step 3: Download history
    if st.button("⬇️ Download History (2021 → now)"):
        df = download_symbol_history(symbol)
        if df is not None:
            st.session_state["last_df"] = df
            st.success(f"Downloaded {len(df)} rows for {symbol} ✅")

    # Step 4: Load from DB
    if st.button("🗄 Load from DB"):
        df = load_candles(symbol, limit=1000)
        if df is not None and not df.empty:
            st.session_state["last_df"] = df
            st.success(f"Loaded {len(df)} rows for {symbol} from DB ✅")
        else:
            st.warning(f"No data found in DB for {symbol}")

    # Step 5: Show chart if data available
    if "last_df" in st.session_state:
        st.subheader(f"📊 Chart for {symbol}")
        plot_candles(st.session_state["last_df"], title=f"{symbol} Candlestick Chart")
