from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    symbol: str = "spy.us"
    source: str = "stooq"
    start: str = "2005-01-01"

    momentum_lookback: int = 126        # 6 month momentum window
    regime_horizon: int = 5             # predict regime 5 trading days ahead
    vol_window: int = 20                # rolling vol window
    trend_window: int = 60              # trend lookback window
    vol_quantile: float = 0.70          # high vol threshold quantile

    regime_threshold: float = 0.60      # probabilistic threshold
    transaction_cost_bps: float = 10.0  # cost per trade

    random_state: int = 42


CFG = Config()