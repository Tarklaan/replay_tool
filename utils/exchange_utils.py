import warnings
warnings.filterwarnings("ignore")

import os
import time
import pandas as pd
from datetime import datetime, timezone, timedelta
import MetaTrader5 as mt5

from replay_tool.utils.utils_db import save_candles

class MetatraderClient:
    def __init__(self, symbol):
        self.symbol = symbol
        self.client = get_exchange_client("metatrader")

    def fetch_data(self, start_datetime, end_datetime, retries=3, retry_delay=5):
        broker_utc_offset = 2

        start_datetime = (start_datetime + timedelta(hours=broker_utc_offset)).replace(tzinfo=timezone.utc)
        end_datetime = (end_datetime + timedelta(hours=broker_utc_offset)).replace(tzinfo=timezone.utc)

        df = None
        for _ in range(retries):
            try:
                data = self.client.copy_rates_range(
                    self.symbol,
                    self.client.TIMEFRAME_M1,
                    start_datetime,
                    end_datetime
                )
                if data is None or len(data) == 0:
                    print(f"No data received for {self.symbol}")
                    return None

                df = pd.DataFrame(data)
                df["datetime"] = pd.to_datetime(df["time"], unit="s", utc=True)
                df["datetime"] = df["datetime"] - pd.Timedelta(hours=broker_utc_offset)
                df.rename(columns={"tick_volume": "volume"}, inplace=True)
                df = df[["datetime", "open", "high", "low", "close", "volume"]]

                df = df.drop(df.index[-1])  # drop incomplete candle
                break

            except Exception as e:
                print(f"Error fetching {self.symbol}: {e}")
                time.sleep(retry_delay)

        self.client.shutdown()
        return df


def get_exchange_client(exchange="metatrader"):
    if exchange == "metatrader":
        mt5_path = r"C:\Program Files\mt5_data\terminal64.exe"
        server = os.getenv("MTRADER_SERVER")
        password = os.getenv("MTRADER_PASSWORD")
        login = int(os.getenv("MTRADER_ACCOUNT", "0"))

        if not mt5.initialize(path=mt5_path, login=login, server=server, password=password):
            raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")

        return mt5
    return None


def get_metatrader_symbols():
    client = get_exchange_client("metatrader")
    symbols = [symbol.name for symbol in client.symbols_get()]
    client.shutdown()
    return symbols


def download_symbol_history(symbol: str, start_year=2021):
    start = datetime(start_year, 1, 1)
    end = datetime.utcnow()

    client = MetatraderClient(symbol)
    df = client.fetch_data(start, end)

    if df is not None:
        save_candles(df, symbol)
        print(f"Saved {len(df)} rows for {symbol} into DB.")
    return df
