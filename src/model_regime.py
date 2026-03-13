import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from src.config import CFG

REGIME_ORDER = ["bull_calm", "bull_volatile", "bear_calm", "bear_volatile"]

FEATURE_COLS = [
    "ret_1d",
    "vol_20d",
    "trend_60d",
    "mom_5d",
    "mom_20d",
    "hl_range",
    "co_return",
    "volchg_5d",
]


def make_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    data["log_close"] = np.log(data["Close"])
    data["ret_1d"] = data["log_close"].diff()
    data["vol_20d"] = data["ret_1d"].rolling(CFG.vol_window).std()
    data["trend_60d"] = data["log_close"].diff(CFG.trend_window)
    data["mom_5d"] = data["log_close"].diff(5)
    data["mom_20d"] = data["log_close"].diff(20)
    data["hl_range"] = (data["High"] - data["Low"]) / data["Close"]
    data["co_return"] = (data["Close"] - data["Open"]) / data["Open"]

    if "Volume" in data.columns:
        data["volchg_5d"] = np.log(data["Volume"]).diff(5)
    else:
        data["volchg_5d"] = 0.0

    return data.dropna().copy()


def label_regimes(features: pd.DataFrame) -> pd.Series:
    vol_thresh = features["vol_20d"].quantile(CFG.vol_quantile)

    vol_regime = np.where(features["vol_20d"] >= vol_thresh, "high_vol", "low_vol")
    trend_regime = np.where(features["trend_60d"] >= 0, "up_trend", "down_trend")

    def combine(tr, vr):
        if tr == "up_trend" and vr == "low_vol":
            return "bull_calm"
        if tr == "up_trend" and vr == "high_vol":
            return "bull_volatile"
        if tr == "down_trend" and vr == "low_vol":
            return "bear_calm"
        return "bear_volatile"

    regimes = [combine(t, v) for t, v in zip(trend_regime, vol_regime)]
    return pd.Series(regimes, index=features.index, name="regime")


def make_target(regime: pd.Series) -> pd.Series:
    return regime.shift(-CFG.regime_horizon).rename("target_regime")


def build_regime_dataset(df: pd.DataFrame) -> pd.DataFrame:
    feat = make_features(df)
    regime = label_regimes(feat)
    target = make_target(regime)

    ds = feat.join(regime).join(target).dropna().copy()
    return ds


def train_regime_model(ds: pd.DataFrame) -> Pipeline:
    X = ds[FEATURE_COLS]
    y = ds["target_regime"]

    clf = RandomForestClassifier(
        n_estimators=500,
        random_state=CFG.random_state,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )

    pipe = Pipeline([("clf", clf)])
    pipe.fit(X, y)
    return pipe


def generate_regime_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    ds = build_regime_dataset(df)

    split = int(len(ds) * 0.8)
    train_ds = ds.iloc[:split].copy()
    full_X = ds[FEATURE_COLS].copy()

    model = train_regime_model(train_ds)

    proba = model.predict_proba(full_X)
    classes = list(model.named_steps["clf"].classes_)

    proba_df = pd.DataFrame(proba, index=ds.index, columns=classes)

    for col in REGIME_ORDER:
        if col not in proba_df.columns:
            proba_df[col] = 0.0

    proba_df = proba_df[REGIME_ORDER]
    return ds.join(proba_df)