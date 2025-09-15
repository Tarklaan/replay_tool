import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def plot_candles(df: pd.DataFrame, title: str = "Candlestick Chart", height: int = 600):
    """
    Plot an interactive candlestick chart with Plotly.

    Args:
        df (pd.DataFrame): Must contain ['datetime', 'open', 'high', 'low', 'close', 'volume']
        title (str): Chart title
        height (int): Chart height in pixels
    """

    if df is None or df.empty:
        st.warning("⚠️ No data available to plot.")
        return

    # Ensure datetime is properly converted
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Create candlestick figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["datetime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="Candles",
            )
        ]
    )

    # Add volume as bar chart (secondary y-axis style)
    fig.add_trace(
        go.Bar(
            x=df["datetime"],
            y=df["volume"],
            name="Volume",
            marker=dict(color="rgba(128,128,128,0.3)"),
            yaxis="y2",
        )
    )

    # Layout adjustments
    fig.update_layout(
        title=title,
        xaxis=dict(title="Time", rangeslider=dict(visible=False)),
        yaxis=dict(title="Price"),
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        height=height,
        template="plotly_dark",  # modern dark theme like TradingView
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)
