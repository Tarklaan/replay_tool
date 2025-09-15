# replay_tool/data/candle_repository.py

import pandas as pd
from sqlalchemy import text
from utils.utils_db import get_engine


def save_candles(df: pd.DataFrame, table_name="candles"):
    """
    Save OHLCV candles into Postgres.
    """
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="append", index=False)


def load_candles(symbol: str, limit: int = 1000, table_name="candles") -> pd.DataFrame:
    """
    Load latest candles for a symbol.
    """
    engine = get_engine()
    query = text(f"""
        SELECT * FROM {table_name}
        WHERE symbol = :symbol
        ORDER BY datetime DESC
        LIMIT :limit
    """)
    with engine.begin() as conn:
        df = pd.read_sql(query, conn, params={"symbol": symbol, "limit": limit})
    return df.sort_values("datetime").reset_index(drop=True)
