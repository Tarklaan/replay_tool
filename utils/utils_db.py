from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import os
import random


def get_engine():
    DB_USER = os.getenv("replay_DB_USER")
    DB_PASS = os.getenv("replay_DB_PASS")
    DB_HOST = os.getenv("replay_DB_HOST")
    DB_PORT = os.getenv("replay_DB_PORT")
    DB_NAME = os.getenv("replay_DB_NAME")

    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(engine_url, echo=False)


def ensure_symbol_table(symbol: str):
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS public."{symbol}" (
                datetime TIMESTAMP NOT NULL,
                open DOUBLE PRECISION,
                high DOUBLE PRECISION,
                low DOUBLE PRECISION,
                close DOUBLE PRECISION,
                volume DOUBLE PRECISION,
                PRIMARY KEY (datetime)
            );
        """))


def save_candles(df: pd.DataFrame, symbol: str):
    ensure_symbol_table(symbol)
    engine = get_engine()

    if not pd.api.types.is_datetime64_any_dtype(df["datetime"]):
        df["datetime"] = pd.to_datetime(df["datetime"])

    if df["datetime"].dt.tz is None:
        df["datetime"] = df["datetime"].dt.tz_localize("UTC")
    else:
        df["datetime"] = df["datetime"].dt.tz_convert("UTC")

    for col in df.select_dtypes(include=["uint64", "int64"]).columns:
        df[col] = df[col].astype("int64")
    for col in df.select_dtypes(include=["float64", "float32"]).columns:
        df[col] = df[col].astype("float64")

    df.to_sql(symbol, engine, if_exists="append", index=False, schema="public")


def get_two_consecutive_trading_days(df):
    trading_days = []
    current_date = df["datetime"].dt.date.min()
    end_date = df["datetime"].dt.date.max()
    
    while current_date <= end_date:
        weekday = pd.to_datetime(current_date).weekday()
        if weekday < 5:
            day_data = df[df["datetime"].dt.date == current_date]
            if not day_data.empty:
                trading_days.append(current_date)
        current_date += pd.Timedelta(days=1)
    
    if len(trading_days) < 2:
        return None, None
    
    random_idx = random.randint(0, len(trading_days) - 2)
    day1 = trading_days[random_idx]
    day2 = trading_days[random_idx + 1]
    
    return day1, day2


def load_random_session(symbol: str):
    df = load_candles(symbol)
    if df.empty:
        return None
    
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    day1, day2 = get_two_consecutive_trading_days(df)
    if day1 is None or day2 is None:
        return None
    
    start_time = pd.to_datetime(f"{day1} 00:00:00")
    end_time = pd.to_datetime(f"{day2} 23:59:59")
    
    session_df = df[(df["datetime"] >= start_time) & (df["datetime"] <= end_time)].copy()
    
    ny_open_day2 = pd.to_datetime(f"{day2} 14:30:00")
    ny_close_day2 = pd.to_datetime(f"{day2} 23:30:00")
    
    session_df["phase"] = "static"
    session_df.loc[
        (session_df["datetime"] >= ny_open_day2) & (session_df["datetime"] <= ny_close_day2),
        "phase"
    ] = "replay"
    
    return session_df


def load_candles(symbol: str, limit: int = 10000) -> pd.DataFrame:
    ensure_symbol_table(symbol)
    engine = get_engine()
    query = f"""
        SELECT * FROM public."{symbol}"
        ORDER BY datetime ASC
        LIMIT {limit};
    """
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)