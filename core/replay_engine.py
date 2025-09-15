import time
import pandas as pd


def replay_session(
    session_df: pd.DataFrame,
    update_chart,
    on_trade=None,
    speed: float = 1.0,
    strategy=None
):
    """
    Replay session candle by candle for backtesting or visualization.

    Args:
        session_df (pd.DataFrame): Historical OHLCV data for the session.
        update_chart (callable): Function that updates the chart.
        on_trade (callable, optional): Hook called when a trade is executed.
        speed (float, optional): Delay between candles (in seconds).
        strategy (callable, optional): Strategy function that decides trades.
    """
    for i in range(len(session_df)):
        window = session_df.iloc[:i + 1]

        # Update chart progressively
        update_chart(window)

        # Run strategy logic (if provided)
        if strategy:
            trades = strategy(window)
            if trades and on_trade:
                for trade in trades:
                    on_trade(trade)

        # Wait before next candle (for live-like replay)
        if speed > 0:
            time.sleep(speed)
