import warnings
warnings.filterwarnings("ignore")

import os
import time
import pandas as pd
from datetime import datetime, timezone, timedelta
import MetaTrader5 as mt5

from replay_tool.utils.utils_db import save_candles


class MetatraderClient:
    """Wrapper for MetaTrader5 data fetching."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.client = get_exchange_client("metatrader")

    def fetch_data(self, start_datetime: datetime, end_datetime: datetime, retries: int = 3, retry_delay: int = 5):
        """
        Fetch OHLCV data from MetaTrader5 within a datetime range.
        Adjusts for broker UTC offset and drops incomplete last candle.
        """
        broker_utc_offset = 2  # Hardcoded offset for broker time

        # Align to broker UTC offset
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
                if not data:
                    print(f"[WARN] No data received for {self.symbol}")
                    return None

                # Convert to DataFrame
                df = pd.DataFrame(data)
                df["datetime"] = pd.to_datetime(df["time"], unit="s", utc=True)
                df["datetime"] = df["datetime"] - pd.Timedelta(hours=broker_utc_offset)
                df.rename(columns={"tick_volume": "volume"}, inplace=True)
                df = df[["datetime", "open", "high", "low", "close", "volume"]]

                # Drop last row (incomplete candle)
                df = df.iloc[:-1]
                break

            except Exception as e:
                print(f"[ERROR] Failed fetching {self.symbol}: {e}")
                time.sleep(retry_delay)

        self.client.shutdown()
        return df


def get_exchange_client(exchange: str = "metatrader"):
    """
    Initialize and return an exchange client.
    Currently supports MetaTrader5 only.
    """
    if exchange == "metatrader":
        # Hardcoded MT5 terminal path
        mt5_path = r"C:\Program Files\mt5_data\terminal64.exe"

        # Credentials still from env (can be hardcoded if you want)
        server = os.getenv("MTRADER_SERVER")
        password = os.getenv("MTRADER_PASSWORD")
        login = int(os.getenv("MTRADER_ACCOUNT", "0"))

        if not mt5.initialize(path=mt5_path, login=login, server=server, password=password):
            raise RuntimeError(f"[CRITICAL] MT5 init failed: {mt5.last_error()}")

        return mt5

    return None


def get_metatrader_symbols():
    """Fetch all available symbols from MetaTrader."""
    client = get_exchange_client("metatrader")
    symbols = [symbol.name for symbol in client.symbols_get()]
    client.shutdown()
    return symbols


def download_symbol_history(symbol: str, start_year: int = 2021):
    """Download full history for a symbol and save into DB."""
    start = datetime(start_year, 1, 1)
    end = datetime.utcnow()

    client = MetatraderClient(symbol)
    df = client.fetch_data(start, end)

    if df is not None:
        save_candles(df, symbol)
        print(f"[INFO] Saved {len(df)} rows for {symbol} into DB.")

    return df
