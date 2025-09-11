import plotly.graph_objects as go

def plot_candles(df):
    """
    Create candlestick chart from DataFrame.
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df['datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        height=600
    )
    return fig
