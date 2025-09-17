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


def ensure_symbol_table(symbol: str):
    """Create table for symbol if it doesn't exist."""
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
    """Save candles into its own symbol table."""
    ensure_symbol_table(symbol)
    engine = get_engine()
    df.to_sql(symbol, engine, if_exists="append", index=False, schema="public")


def load_candles(symbol: str, limit: int = 1000) -> pd.DataFrame:
    ensure_symbol_table(symbol)
    engine = get_engine()
    query = f"""
        SELECT * FROM public."{symbol}"
        ORDER BY datetime ASC
        LIMIT {limit};
    """
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
