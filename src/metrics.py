import numpy as np
import pandas as pd


def annualized_return(returns: pd.Series) -> float:
    compounded = (1 + returns).prod()
    n_years = len(returns) / 252
    return compounded ** (1 / n_years) - 1 if n_years > 0 else np.nan


def annualized_volatility(returns: pd.Series) -> float:
    return returns.std() * np.sqrt(252)


def sharpe_ratio(returns: pd.Series) -> float:
    vol = annualized_volatility(returns)
    if vol == 0:
        return np.nan
    return annualized_return(returns) / vol


def max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    return drawdown.min()


def turnover(position: pd.Series) -> float:
    return position.diff().abs().fillna(0).sum() / len(position)


def exposure(position: pd.Series) -> float:
    return position.mean()


def number_of_trades(position: pd.Series) -> int:
    return int(position.diff().abs().fillna(0).sum())


def summarize_backtest(bt: pd.DataFrame) -> pd.Series:
    r = bt["net_strategy_return"]
    p = bt["position"]
    eq = bt["equity_curve"]

    return pd.Series({
        "annualized_return": annualized_return(r),
        "annualized_volatility": annualized_volatility(r),
        "sharpe_ratio": sharpe_ratio(r),
        "max_drawdown": max_drawdown(eq),
        "turnover": turnover(p),
        "exposure": exposure(p),
        "number_of_trades": number_of_trades(p),
    })