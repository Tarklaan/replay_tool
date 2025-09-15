import pandas as pd
from replay_tool.utils.utils_db import save_candles

def load_data(path: str, save_to_db: bool = True):
    df = pd.read_csv(path, sep=";")

    # Ensure datetime column
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
    else:
        raise ValueError("CSV must contain a 'datetime' column")

    # Save to DB if requested
    if save_to_db:
        save_candles(df)

    return df


def extract_sessions(df: pd.DataFrame, start="09:30", end="16:00") -> dict:
    """
    Extract New York sessions from OHLCV data.
    Returns {date: DataFrame} dictionary.
    """
    df = df.set_index("datetime")
    df = df.between_time(start, end)
    sessions = df.groupby(df.index.date)
    return {date: group.reset_index() for date, group in sessions}
