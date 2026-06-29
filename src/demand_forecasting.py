"""Batch retail demand forecasting pipeline for M5-style synthetic data."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Tuple

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_sales.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "forecast_output.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.25
ROLLING_WINDOW = 7


def load_sales(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load sales data with typed date parsing and validation."""
    try:
        sales = pd.read_csv(path, parse_dates=["date"])
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Sales input file not found: {path}") from exc
    required = {"date", "store_id", "product_id", "category", "units_sold", "sell_price", "promotion_flag", "snap_flag"}
    missing = required.difference(sales.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return sales.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)


def build_features(sales: pd.DataFrame) -> pd.DataFrame:
    """Create lag, rolling, calendar, and SNAP features for forecasting."""
    featured = sales.copy()
    group_cols = ["store_id", "product_id"]
    featured["day_of_week"] = featured["date"].dt.dayofweek
    featured["week_of_year"] = featured["date"].dt.isocalendar().week.astype(int)
    featured["month"] = featured["date"].dt.month
    # Lag features simulate the information available before the next planning cycle.
    featured["lag_1_units"] = featured.groupby(group_cols)["units_sold"].shift(1)
    featured["lag_7_units"] = featured.groupby(group_cols)["units_sold"].shift(7)
    # Rolling demand smooths noisy daily sales while preserving local trend direction.
    featured["rolling_7_units"] = featured.groupby(group_cols)["units_sold"].transform(
        lambda series: series.shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean()
    )
    fill_value = featured["units_sold"].median()
    return featured.fillna({"lag_1_units": fill_value, "lag_7_units": fill_value, "rolling_7_units": fill_value})


def train_model(featured: pd.DataFrame) -> Tuple[RandomForestRegressor, dict[str, float]]:
    """Train a baseline tree model and return validation metrics."""
    model_frame = pd.get_dummies(
        featured[["store_id", "product_id", "category", "city", "sell_price", "promotion_flag", "snap_flag", "day_of_week", "week_of_year", "month", "lag_1_units", "lag_7_units", "rolling_7_units", "units_sold"]],
        columns=["store_id", "product_id", "category", "city"],
        drop_first=False,
    )
    features = model_frame.drop(columns=["units_sold"])
    target = model_frame["units_sold"]
    train_x, test_x, train_y, test_y = train_test_split(features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    model = RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=RANDOM_STATE)
    start_time = perf_counter()
    model.fit(train_x, train_y)
    training_time = perf_counter() - start_time
    predictions = model.predict(test_x)
    # Metrics mirror the README model comparison table for recruiter verification.
    metrics = {
        "mae": float(mean_absolute_error(test_y, predictions)),
        "rmse": float(mean_squared_error(test_y, predictions) ** 0.5),
        "r2": float(r2_score(test_y, predictions)),
        "training_time": float(training_time),
    }
    return model, metrics


def write_forecast_output(featured: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """Score all rows and write a dashboard-ready forecast output file."""
    scoring_frame = pd.get_dummies(
        featured[["store_id", "product_id", "category", "city", "sell_price", "promotion_flag", "snap_flag", "day_of_week", "week_of_year", "month", "lag_1_units", "lag_7_units", "rolling_7_units"]],
        columns=["store_id", "product_id", "category", "city"],
        drop_first=False,
    )
    output = featured.copy()
    output["forecast_units"] = model.predict(scoring_frame).round(0).astype(int)
    output["forecast_error"] = output["units_sold"] - output["forecast_units"]
    # A positive demand gap becomes a direct replenishment review signal.
    output["stockout_risk_flag"] = (output["forecast_units"] > output["rolling_7_units"] * 1.10).astype(int)
    output.to_csv(OUTPUT_PATH, index=False)
    return output


def main() -> None:
    """Execute the complete batch forecasting workflow."""
    sales = load_sales()
    featured = build_features(sales)
    model, metrics = train_model(featured)
    write_forecast_output(featured, model)
    print("Retail demand forecasting summary")
    print(f"Rows scored: {len(featured)}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"R2: {metrics['r2']:.2f}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
