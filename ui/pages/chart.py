import streamlit as st
import pandas as pd
import time
import sys
import os
import warnings

warnings.filterwarnings("ignore")

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from replay_tool.ui.chart import plot_candles, plot_replay_candles, resample_data

st.set_page_config(
    page_title="Chart", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "chart_data" not in st.session_state:
    st.error("No chart data found. Please load a chart first.")
    if st.button("← Back to Home"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state["chart_data"]
symbol = st.session_state["symbol"]
current_timeframe = st.session_state["timeframe"]

if df is None or df.empty:
    st.error("Chart data is empty!")
    if st.button("← Back to Home"):
        st.switch_page("app.py")
    st.stop()

st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .stButton > button {
        height: 2.5rem;
    }
    .toolbar {
        background-color: #0e1117;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 8])

with col1:
    if st.button("← Home"):
        st.switch_page("app.py")

with col2:
    timeframe = st.selectbox("Timeframe", ["1M", "5M", "15M", "30M", "1H", "4H", "1D"], 
                            index=["1M", "5M", "15M", "30M", "1H", "4H", "1D"].index(current_timeframe),
                            key="timeframe_selector",
                            label_visibility="collapsed")

if timeframe != current_timeframe:
    original_df = st.session_state["original_data"]
    resampled_df = resample_data(original_df, timeframe)
    st.session_state["chart_data"] = resampled_df
    st.session_state["timeframe"] = timeframe
    st.session_state["replay_active"] = False
    st.session_state["replay_paused"] = False
    st.session_state["replay_index"] = 0
    df = resampled_df

with col3:
    if st.button("🎬 Replay"):
        st.session_state["replay_active"] = True
        st.session_state["replay_paused"] = False
        st.session_state["replay_index"] = 0

with col4:
    if st.button("⏸️ Pause"):
        if st.session_state.get("replay_active", False):
            st.session_state["replay_paused"] = not st.session_state.get("replay_paused", False)

with col5:
    if st.button("🔄 Reset"):
        st.session_state["replay_active"] = False
        st.session_state["replay_paused"] = False
        st.session_state["replay_index"] = 0

static_data = df[df["phase"] == "static"]
replay_data = df[df["phase"] == "replay"]

if "replay_active" not in st.session_state:
    st.session_state["replay_active"] = False
    st.session_state["replay_paused"] = False
    st.session_state["replay_index"] = 0

with st.sidebar:
    st.header("Chart Info")
    st.write(f"**Symbol:** {symbol}")
    st.write(f"**Timeframe:** {timeframe}")
    st.write(f"**Total Candles:** {len(df)}")
    st.write(f"**Static Candles:** {len(static_data)}")
    st.write(f"**Replay Candles:** {len(replay_data)}")
    
    if st.session_state.get("replay_active", False):
        st.write(f"**Current:** {st.session_state['replay_index']}")
    
    st.markdown("---")
    st.header("Drawing Tools")
    st.write("**Available in toolbar:**")
    st.write("📐 Line Tool")
    st.write("⬜ Rectangle Tool") 
    st.write("🗑️ Erase Tool")
    
    st.markdown("---")
    st.header("Position Tools")
    
    current_price = df.iloc[-1]["close"] if not df.empty else 0
    st.write(f"**Current Price:** {current_price:.2f}")
    
    col_long, col_short = st.columns(2)
    
    with col_long:
        if st.button("🟢 LONG", use_container_width=True, type="primary"):
            st.success(f"Long at {current_price:.2f}")
            st.balloons()
    
    with col_short:
        if st.button("🔴 SHORT", use_container_width=True):
            st.error(f"Short at {current_price:.2f}")
    
    st.markdown("---")
    st.write("**Chart Controls:**")
    st.write("• Pan: Click + Drag")
    st.write("• Zoom: Scroll wheel") 
    st.write("• Reset: Double click")
    st.write("• Draw: Use toolbar tools")

chart_container = st.container()

with chart_container:
    try:
        if st.session_state["replay_active"] and not replay_data.empty:
            plot_replay_candles(
                static_data, 
                replay_data, 
                st.session_state["replay_index"], 
                title=f"{symbol} • {timeframe} • Replay Mode",
                height=700
            )
            
            if not st.session_state.get("replay_paused", False) and st.session_state["replay_index"] < len(replay_data) - 1:
                st.session_state["replay_index"] += 1
                time.sleep(0.3)
                st.rerun()
            elif st.session_state["replay_index"] >= len(replay_data) - 1:
                st.session_state["replay_active"] = False
                st.success("✅ Replay completed!")
        else:
            plot_candles(df, title=f"{symbol} • {timeframe}", height=700)
    except Exception as e:
        st.error(f"Error rendering chart: {str(e)}")
        st.write("Debug info:")
        st.write(f"DataFrame shape: {df.shape}")
        st.write(f"DataFrame columns: {df.columns.tolist()}")
        st.write(f"First few rows:")
        st.dataframe(df.head())

if not replay_data.empty:
    progress_percentage = int((st.session_state['replay_index'] / len(replay_data)) * 100)
    st.progress(progress_percentage / 100)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"📊 Replay Progress: {st.session_state['replay_index']}/{len(replay_data)} ({progress_percentage}%)")