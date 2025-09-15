from sqlalchemy import create_engine, text
import pandas as pd
import os

def get_engine():
    DB_USER = os.getenv("replay_DB_USER")
    DB_PASS = os.getenv("replay_DB_PASS")
    DB_HOST = os.getenv("replay_DB_HOST")
    DB_PORT = os.getenv("replay_DB_PORT")
    DB_NAME = os.getenv("replay_DB_NAME")

    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(engine_url, echo=False)


def save_dataframe(df: pd.DataFrame, table_name: str, if_exists: str = "append"):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def load_dataframe(query: str) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)


def save_candles(df: pd.DataFrame, symbol: str):
    """Save candles with symbol info"""
    df["symbol"] = symbol
    save_dataframe(df, "candles")


def load_candles(symbol: str, limit: int = 1000) -> pd.DataFrame:
    query = f"""
        SELECT * FROM candles 
        WHERE symbol = '{symbol}' 
        ORDER BY datetime ASC 
        LIMIT {limit};
    """
    return load_dataframe(query)
