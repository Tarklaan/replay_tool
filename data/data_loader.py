# replay_tool/data/data_loader.py

import pandas as pd
from replay_tool.utils.utils_db import save_candles


def load_data(path: str, save_to_db: bool = True):
    """
    Load OHLCV data from a CSV file.
    Optionally save it to the database.
    """
    df = pd.read_csv(path, sep=";")

    # Ensure datetime column exists and is in datetime format
    if "datetime" not in df.columns:
        raise ValueError("CSV must contain a 'datetime' column")

    df["datetime"] = pd.to_datetime(df["datetime"])

    # Sort by datetime to avoid replay issues
    df = df.sort_values("datetime").reset_index(drop=True)

    # Save to DB if requested
    if save_to_db:
        save_candles(df)

    return df


def extract_sessions(df: pd.DataFrame, start="09:30", end="16:00") -> dict:
    """
    Extract sessions between given times (default: New York session).
    Returns a dictionary {date: DataFrame}.
    """
    df = df.copy()
    df = df.set_index("datetime")

    # Filter by time window (intraday)
    session_df = df.between_time(start, end)

    # Group into sessions by calendar date
    sessions = session_df.groupby(session_df.index.date)

    # Convert back to dict of DataFrames
    return {date: group.reset_index() for date, group in sessions}
