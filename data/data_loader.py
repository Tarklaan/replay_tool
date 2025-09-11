import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load OHLCV data from CSV.
    CSV must have: datetime, open, high, low, close, volume
    """
    df = pd.read_csv(filepath)
    df['datetime'] = pd.to_datetime(df['datetime'])
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
