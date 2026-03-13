# Evaluating a Regime-Filtered Momentum Strategy

Testing whether a probabilistic market regime filter improves the performance of a 6-month momentum strategy on SPY.

## Overview

This project evaluates whether adding a probabilistic market regime filter improves the performance of a 6-month momentum trading strategy.

The baseline strategy goes long SPY when its 6-month momentum is positive and otherwise holds cash. The treatment strategy applies the same momentum rule, but only enters the market when the predicted probability of a favorable market regime (`bull_calm`) exceeds a specified threshold.

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

## Backtest Rules

- Sample start: 2005
- Signal evaluation frequency: daily
- Position rules: long or cash
- Execution assumption: signals are shifted by one day

## Evaluation Metrics

The following metrics are used to compare the baseline and optimized strategies.

- total return
- annualized return
- annualized volatility
- sharpe ratio
- max drawdown
- turnover
- exposure
- number of trades

## Initial Results

In the initial backtest, using a probabilistic threshold of 0.6 for if the regime is determined to be 'bull_calm', the regime optimized strategy outperformed the baseline momentum strategy on both return and risk adjusted metrics.

| Metric | Momentum | Filtered |
|---|---:|---:|
| Annualized return | 7.1% | 10.4% |
| Annualized volatility | 11.5% | 7.9% |
| Sharpe ratio | 0.61 | 1.31 |
| Max drawdown | -24.0% | -15.7% |
| Exposure | 74.6% | 56.6% |

The results suggest that the regime optimized strategy improves the performance by reducing exposure during periods where the market is unfavorable.

## Threshold Sensitivity

The probbilistic threshold was tested across multiple values: 0.5, 0.6, 0.7, 0.8

The results showed a tradeoff where the lower thresholds resulted in high return and higher exposure, while the higher thresholds reduced drawdown and volatility.
Ultimately a threshold around 0.5-0.6 produced the strongest Sharpe ratios.





step1: define baseline strategy - 6 month momentum
treatment strategy - as baseline but adding regime probability (testing different prob thresholds)

step2: trading rules - signal computed using data up to day n, then trade is executed at next day close
signal at close(n)
position active at close(n+1)
also include a small transaction cost per trade

step3: regime signal

step4: evaluation metrics
performance - cumulative return and annualized return
risk - annualized volatility and max drawdown
risk-adjusted - sharpe ratio, sortino ratio
strategy behavior - turnover, exposure (% of time invested), avg trade return

step5: statistical analysis
bootstrap sharpe difference

step6: diagnostic analysis
what is the momentum performance depending on market regime

step7: sensitivity analysis
testing different probability thresholds, and different lookbacks for momentum strategy

