import pandas as pd

from src.config import CFG


def run_backtest(df: pd.DataFrame, position: pd.Series) -> pd.DataFrame:
    out = df.copy()
    out["asset_return"] = out["Close"].pct_change().fillna(0.0)

    # strategy position - shifted upstream
    out["position"] = position.reindex(out.index).fillna(0).astype(float)

    out["gross_strategy_return"] = out["position"] * out["asset_return"]

    trades = out["position"].diff().abs().fillna(0.0)
    cost = trades * (CFG.transaction_cost_bps / 10000.0)

    out["transaction_cost"] = cost
    out["net_strategy_return"] = out["gross_strategy_return"] - out["transaction_cost"]

    out["equity_curve"] = (1 + out["net_strategy_return"]).cumprod()
    return out