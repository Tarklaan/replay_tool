import streamlit as st
from replay_tool.utils.exchange_utils import get_metatrader_symbols, download_symbol_history
from replay_tool.ui.chart import resample_data
from replay_tool.utils.utils_db import load_random_session

st.set_page_config(page_title="Trading Replay Tool", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_instruments():
    return get_metatrader_symbols()

if "symbols" not in st.session_state:
    with st.spinner("Loading instruments..."):
        st.session_state["symbols"] = load_instruments()
    st.success(f"Loaded {len(st.session_state['symbols'])} instruments ✅")

st.title("📈 Trading Replay Tool")

col1, col2 = st.columns([1, 1])
with col1:
    symbol = st.selectbox("🎯 Select a symbol", st.session_state["symbols"])
with col2:
    timeframe = st.selectbox("⏱️ Timeframe", ["1M", "5M", "15M", "30M", "1H", "4H", "1D"], index=1)

st.markdown("---")

if st.button("📊 Load Chart", type="primary", use_container_width=True):
    try:
        with st.spinner(f"Loading {symbol} data..."):
            df = load_random_session(symbol)
            if df is None or df.empty:
                st.info(f"No data found in DB for {symbol}, downloading history...")
                df = download_symbol_history(symbol)
                if df is not None and not df.empty:
                    df = load_random_session(symbol)
            if df is not None and not df.empty:
                resampled_df = resample_data(df, timeframe)
                st.session_state["chart_data"] = resampled_df
                st.session_state["original_data"] = df
                st.session_state["symbol"] = symbol
                st.session_state["timeframe"] = timeframe
                st.session_state["replay_active"] = False
                st.session_state["replay_paused"] = False
                st.session_state["replay_index"] = 0
                st.switch_page("pages/chart.py")
            else:
                st.error(f"Could not load data for {symbol}")
    except Exception as e:
        st.error(f"Error loading chart: {e}")
