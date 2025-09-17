# replay_tool/data/trade_repository.py

import pandas as pd
from sqlalchemy import text
from replay_tool.utils.utils_db import get_engine


def save_trade(trade: dict, table_name="trades"):
    """
    Save a single manual trade (dict with symbol, side, entry, exit, pnl, etc.).
    """
    df = pd.DataFrame([trade])
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="append", index=False)


def load_trades(symbol: str = None, table_name="trades") -> pd.DataFrame:
    """
    Load trades, optionally filter by symbol.
    """
    engine = get_engine()
    query = f"SELECT * FROM {table_name}"
    params = {}

    if symbol:
        query += " WHERE symbol = :symbol"
        params["symbol"] = symbol

    with engine.begin() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    return df
