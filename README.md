# regime-filtered-momentum

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

