import pandas as pd


def gann_50_line(df: pd.DataFrame):
    """
    Calculate the 50% retracement line from session high/low.
    """
    high = df["High"].max()
    low = df["Low"].min()
    return (high + low) / 2


def gann_square_levels(df: pd.DataFrame, long=True):
    """
    Create Gann square levels around the 50% line.
    Long = above 50%, Short = below 50%.
    """
    mid = gann_50_line(df)

    if long:
        return {
            "mid": mid,
            "square_up": mid * 1.25,
            "square_down": mid * 0.75,
        }
    else:
        return {
            "mid": mid,
            "square_up": mid * 0.75,
            "square_down": mid * 1.25,
        }
