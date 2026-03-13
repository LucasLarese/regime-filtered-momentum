# Evaluating a Regime Filtered Momentum Strategy

Testing whether a probabilistic market regime filter improves the performance of a 6-month momentum strategy on SPY.

## Overview

This project evaluates whether adding a probabilistic market regime filter improves the performance of a 6-month momentum trading strategy.

The baseline strategy goes long SPY when its 6-month momentum is positive and otherwise holds cash. The treatment strategy applies the same momentum rule, but only enters the market when the predicted probability of a favorable market regime 'bull_calm' exceeds a specified threshold.

The aim is to test whether regime contextual filtering improves return quality, reduces drawdowns, and produces better risk-adjusted performance.

## Strategy Comparison

### Baseline Strategy
- Compute the 6-month momentum using a 126 trading day lookback
- Go long SPY if momentum > 0
- Otherwise hold cash

### Optimized Strategy
- Start with same 6-month momentum strategy
- Only go long when the predicted probability of 'bull_calm' is above a specified threshold
- Otherwise hold cash

## Regime Model

The regime filter is based on a probabilistic classifier trained to predict future market regimes from time-series features. The model is based off the project 'market-regime-detection'. Brief description of the model below.

Regimes are defined using:
- trend
- volatility

The model outputs probabilities for:
- bull_calm
- bull_volatile
- bear_calm
- bear_volatile

The optimized trading strategy uses the probability of 'bull_calm' as a filter to decide when momentum signals should be trusted.

When the strategy changes position, a 10 basis points (0.10%) cost is applied to approximate realistic trading conditions.

## Backtest Rules

- Sample start: 2005
- Signal evaluation frequency: daily
- Position rules: long or cash
- Execution assumption: signals are shifted by one day

Signals are computed using information available at day t, and positions are applied at day t + 1.

## Evaluation Metrics

The following metrics are used to compare the baseline and optimized strategies.

### Performance
- total return
- annualized return

### Risk
- annualized volatility
- max drawdown

### Risk-adjusted Performance
- sharpe ratio

### Strategy Behavior
- turnover
- exposure (pct of time invested)
- number of trades

## Initial Results

In the initial backtest, using a probabilistic threshold of 0.6 for the 'bull_calm' regime, the regime filtered strategy outperformed the baseline momentum strategy on both return and risk adjusted metrics.

| Metric | Momentum | Filtered |
|---|---:|---:|
| Annualized return | 7.1% | 10.4% |
| Annualized volatility | 11.5% | 7.9% |
| Sharpe ratio | 0.61 | 1.31 |
| Max drawdown | -24.0% | -15.7% |
| Exposure | 74.6% | 56.6% |

The results suggest that the regime optimized strategy improves the performance by reducing exposure during periods where the market is unfavorable.

## Comparison with Buying and Holding SPY

While the regime filtered strategy improves substantially upon the baseline momentum strategy, buying and holding SPY seems to remain a strong benchmark.

This can be expected given the strong long-term upward trend of the US equity market over the period sampled in this project (2005-present). The baseline momentum strategy frequently exits the market during short term pullbacks, which can cause it to miss portions of sustained bull markets.

However, the regime filtered strategy demonstrates meaningful improvements in comparison to the baseline momentum strategy with a higher annalized return, higher Sharpe ratio and lower volatility. This signals that the regime filter improves the quality of the momentum signal by reducing exposure during unfavorable market trends while still investing during strong market trends.

## Threshold Sensitivity

The probabilistic threshold was tested across multiple values: 0.5, 0.6, 0.7, 0.8

The results showed a tradeoff where the lower thresholds resulted in high return and higher exposure, while the higher thresholds reduced drawdown and volatility.
Ultimately a threshold around 0.5-0.6 produced the strongest Sharpe ratios.

## Repo Structure
```text
regime-filtered-momentum/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_strategy_design.ipynb
│   └── 02_backtest_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data.py
│   ├── regime.py
│   ├── signals.py
│   ├── strategy.py
│   ├── backtest.py
│   ├── metrics.py
│   └── plotting.py
└── reports/
    └── figures/
```

## Possible Future Extensions

- testing additional momentum lookback windows
- applying the framework to other ETFs
- sensitivity to transaction costs
