from sqlalchemy import create_engine, text
import pandas as pd
import os


def get_engine():
    """
    Create a SQLAlchemy engine for PostgreSQL using env variables.
    """
    DB_USER = os.getenv("replay_DB_USER")
    DB_PASS = os.getenv("replay_DB_PASS")
    DB_HOST = os.getenv("replay_DB_HOST", "localhost")
    DB_PORT = os.getenv("replay_DB_PORT", "5432")
    DB_NAME = os.getenv("replay_DB_NAME")

    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(engine_url, echo=False, future=True)


def save_dataframe(df: pd.DataFrame, table_name: str, if_exists: str = "append"):
    """
    Save a DataFrame to the given PostgreSQL table.
    Defaults to appending data.
    """
    if df.empty:
        print(f"[WARN] Tried to save empty DataFrame into {table_name}. Skipping.")
        return

    engine = get_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def load_dataframe(query: str) -> pd.DataFrame:
    """
    Run a SQL query and return results as a DataFrame.
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)


def save_candles(df: pd.DataFrame, symbol: str):
    """
    Save OHLCV candles into the 'candles' table, tagging them with the symbol.
    """
    if df.empty:
        print(f"[WARN] No candles to save for {symbol}. Skipping.")
        return

    df["symbol"] = symbol
    save_dataframe(df, "candles")


def load_candles(symbol: str, limit: int = 1000) -> pd.DataFrame:
    """
    Load candles for a given symbol from the DB.
    Results are ordered by datetime ASC and limited.
    """
    query = f"""
        SELECT *
        FROM candles
        WHERE symbol = :symbol
        ORDER BY datetime ASC
        LIMIT :limit;
    """
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params={"symbol": symbol, "limit": limit})
