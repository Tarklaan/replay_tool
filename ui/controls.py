import streamlit as st
from utils.exchange_utils import get_metatrader_symbols


def instruments_control():
    """
    UI control for loading and selecting trading instruments.
    """
    if st.button("🔄 Load Instruments"):
        symbols = get_metatrader_symbols()
        st.session_state["symbols"] = symbols
        st.success(f"Loaded {len(symbols)} instruments ✅")

    symbol = None
    if "symbols" in st.session_state:
        symbol = st.selectbox("🎯 Select a symbol", st.session_state["symbols"])
    return symbol


def history_control(symbol: str):
    """
    UI control for downloading or loading historical data.
    """
    download = st.button("⬇️ Download History (2021 → now)")
    load_db = st.button("🗄 Load from DB")
    return download, load_db


def session_picker_control():
    """
    UI control for selecting which session to replay.
    (e.g., New York, London, Tokyo)
    """
    session_type = st.selectbox(
        "⏰ Select session",
        ["New York", "London", "Tokyo", "Full Day"]
    )
    return session_type


def indicator_controls():
    """
    UI controls for toggling basic indicators.
    """
    st.sidebar.header("📊 Indicators")
    show_ma = st.sidebar.checkbox("Show Moving Averages", value=True)
    show_vwap = st.sidebar.checkbox("Show VWAP", value=False)
    return {"ma": show_ma, "vwap": show_vwap}
