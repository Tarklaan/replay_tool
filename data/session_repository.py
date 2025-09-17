# replay_tool/data/session_repository.py

import pandas as pd
from sqlalchemy import text
from replay_tool.utils.utils_db import get_engine


def save_session(date: str, df: pd.DataFrame, table_name="sessions"):
    """
    Save extracted session candles to DB.
    """
    df = df.copy()
    df["session_date"] = date
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="append", index=False)


def load_session(date: str, table_name="sessions") -> pd.DataFrame:
    """
    Load a specific session from DB.
    """
    engine = get_engine()
    query = text(f"""
        SELECT * FROM {table_name}
        WHERE session_date = :date
        ORDER BY datetime ASC
    """)
    with engine.begin() as conn:
        df = pd.read_sql(query, conn, params={"date": date})
    return df
