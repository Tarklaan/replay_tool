import time

def replay_session(session_df, update_chart, speed=1.0):
    """
    Replay session candle by candle.
    update_chart: function to update the chart
    speed: seconds per candle (e.g. 0.5 = faster playback)
    """
    for i in range(len(session_df)):
        window = session_df.iloc[:i+1]
        update_chart(window)
        time.sleep(speed)
