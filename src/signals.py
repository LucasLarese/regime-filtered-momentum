import numpy as np
import pandas as pd

from src.config import CFG


def six_month_momentum_signal(df: pd.DataFrame) -> pd.Series:
    momentum = df["Close"].pct_change(CFG.momentum_lookback)
    signal = (momentum > 0).astype(int)
    return signal.rename("momentum_signal")


def regime_filtered_signal(df_with_regime: pd.DataFrame) -> pd.Series:
    momentum = df_with_regime["Close"].pct_change(CFG.momentum_lookback)
    base_signal = (momentum > 0).astype(int)

    regime_filter = (df_with_regime["bull_calm"] > CFG.regime_threshold).astype(int)

    signal = (base_signal * regime_filter).astype(int)
    return signal.rename("filtered_signal")