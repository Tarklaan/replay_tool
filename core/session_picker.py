import random
import pandas as pd
from typing import Dict, Tuple


def pick_random_session(sessions: Dict[str, pd.DataFrame]) -> Tuple[str, pd.DataFrame]:
    """
    Pick a random trading session from a sessions dictionary.

    Args:
        sessions (dict): A mapping {date: DataFrame}, where
                         - key is the session date (str or datetime)
                         - value is the OHLCV DataFrame for that session.

    Returns:
        tuple: (date, DataFrame) for the chosen session.
    """
    if not sessions:
        raise ValueError("No sessions available to pick from.")

    date = random.choice(list(sessions.keys()))
    return date, sessions[date]
