import streamlit as st
import pandas as pd
import time
import sys
import os

# Add the parent directory to Python path so we can import from replay_tool
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_loader import load_data, extract_sessions
from core.session_picker import pick_random_session
from core.replay_engine import replay_session
from ui.chart import plot_candles

# Load data once
DATA_PATH = "data/sample_data.csv"
df = load_data(DATA_PATH)
sessions = extract_sessions(df)

st.title("📈 NY Session Replay Tool (NQ & ES)")

# Speed control
speed = st.slider("Replay Speed (sec per candle)", 0.1, 2.0, 0.5, 0.1)

if st.button("▶ Start Replay"):
    session_date, session_df = pick_random_session(sessions)
    st.write(f"Replaying New York session: **{session_date}**")

    chart = st.empty()

    for i in range(len(session_df)):
        fig = plot_candles(session_df.iloc[:i+1])
        chart.plotly_chart(fig, use_container_width=True)
        time.sleep(speed)