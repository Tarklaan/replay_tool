import streamlit as st
import pandas as pd
import time
from replay_tool.utils.exchange_utils import get_metatrader_symbols, download_symbol_history
from replay_tool.ui.chart import plot_candles, plot_replay_candles, resample_data
from replay_tool.utils.utils_db import load_candles, load_random_session

st.set_page_config(page_title="Replay Tool", layout="wide")
st.title("📈 Trading Replay Tool")

if st.button("🔄 Load Instruments"):
    symbols = get_metatrader_symbols()
    st.session_state["symbols"] = symbols
    st.success(f"Loaded {len(symbols)} instruments ✅")

if "symbols" in st.session_state:
    symbol = st.selectbox("🎯 Select a symbol", st.session_state["symbols"])
    
    col1, col2 = st.columns([1, 1])
    with col1:
        timeframe = st.selectbox("⏱️ Timeframe", ["1M", "5M", "15M", "30M", "1H", "4H", "1D"], index=1)
    
    with col2:
        if st.button("📊 Load Chart (2-Day Trading Session)"):
            try:
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
                    st.success(f"Loaded {len(resampled_df)} candles for {symbol} ({timeframe}) ✅")
                else:
                    st.warning(f"Could not load or download data for {symbol}.")

            except Exception as e:
                st.error(f"Error loading chart: {e}")

if "chart_data" in st.session_state:
    if st.session_state.get("timeframe") != timeframe:
        original_df = st.session_state["original_data"]
        resampled_df = resample_data(original_df, timeframe)
        st.session_state["chart_data"] = resampled_df
        st.session_state["timeframe"] = timeframe
        st.session_state["replay_active"] = False
        st.session_state["replay_paused"] = False
        st.session_state["replay_index"] = 0

    df = st.session_state["chart_data"]
    symbol = st.session_state["symbol"]
    
    st.subheader(f"📊 Chart for {symbol} ({timeframe})")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎬 Start Replay"):
            st.session_state["replay_active"] = True
            st.session_state["replay_paused"] = False
            st.session_state["replay_index"] = 0
    
    with col2:
        if st.button("⏸️ Pause/Resume"):
            if st.session_state.get("replay_active", False):
                st.session_state["replay_paused"] = not st.session_state.get("replay_paused", False)
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state["replay_active"] = False
            st.session_state["replay_paused"] = False
            st.session_state["replay_index"] = 0

    if "replay_active" not in st.session_state:
        st.session_state["replay_active"] = False
        st.session_state["replay_paused"] = False
        st.session_state["replay_index"] = 0

    static_data = df[df["phase"] == "static"]
    replay_data = df[df["phase"] == "replay"]
    
    if st.session_state["replay_active"] and not replay_data.empty:
        plot_replay_candles(static_data, replay_data, st.session_state["replay_index"], title=f"{symbol} Replay ({timeframe})")
        
        if not st.session_state.get("replay_paused", False) and st.session_state["replay_index"] < len(replay_data) - 1:
            st.session_state["replay_index"] += 1
            time.sleep(0.5)
            st.rerun()
        elif st.session_state["replay_index"] >= len(replay_data) - 1:
            st.session_state["replay_active"] = False
            st.success("Replay completed!")
    else:
        if st.session_state["replay_index"] == 0:
            plot_candles(df, title=f"{symbol} Full Chart ({timeframe})")
        else:
            plot_replay_candles(static_data, replay_data, st.session_state["replay_index"], title=f"{symbol} Replay (Paused) ({timeframe})")
    
    if not replay_data.empty:
        progress_percentage = int((st.session_state['replay_index'] / len(replay_data)) * 100)
        st.progress(progress_percentage / 100)
        st.info(f"Replay Progress: {st.session_state['replay_index']}/{len(replay_data)} candles ({progress_percentage}%)")