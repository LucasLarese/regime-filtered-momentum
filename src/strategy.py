import pandas as pd


def positions_from_signal(signal: pd.Series) -> pd.Series:
    # shift by 1 day to avoid look-ahead bias
    return signal.shift(1).fillna(0).astype(int).rename("position")