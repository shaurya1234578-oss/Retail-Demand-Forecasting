"""Baseline demand forecasting workflow for retail inventory analytics."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "sample_sales.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "forecast_output.csv"


def load_sales(path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load sales data and parse date fields."""
    return pd.read_csv(path, parse_dates=["date"])


def build_features(sales: pd.DataFrame) -> pd.DataFrame:
    """Create forecasting features from retail sales history."""
    featured = sales.sort_values(["store_id", "product_id", "date"]).copy()
    group_cols = ["store_id", "product_id"]
    featured["day_of_week"] = featured["date"].dt.dayofweek
    featured["lag_1_units"] = featured.groupby(group_cols)["units_sold"].shift(1)
    featured["rolling_3_units"] = featured.groupby(group_cols)["units_sold"].transform(
        lambda series: series.shift(1).rolling(window=3, min_periods=1).mean()
    )
    featured["lag_1_units"] = featured["lag_1_units"].fillna(featured["units_sold"].median())
    featured["rolling_3_units"] = featured["rolling_3_units"].fillna(featured["units_sold"].median())
    return featured


def train_forecast_model(featured: pd.DataFrame) -> tuple[RandomForestRegressor, float]:
    """Train a baseline random forest model and return validation MAE."""
    model_frame = pd.get_dummies(
        featured[
            [
                "store_id",
                "product_id",
                "category",
                "price",
                "promotion_flag",
                "day_of_week",
                "lag_1_units",
                "rolling_3_units",
                "units_sold",
            ]
        ],
        columns=["store_id", "product_id", "category"],
        drop_first=False,
    )
    features = model_frame.drop(columns=["units_sold"])
    target = model_frame["units_sold"]
    train_x, test_x, train_y, test_y = train_test_split(
        features, target, test_size=0.30, random_state=42
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_x, train_y)
    predictions = model.predict(test_x)
    return model, mean_absolute_error(test_y, predictions)


def create_forecast_output(featured: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """Generate forecast output and business-friendly inventory recommendations."""
    scoring_frame = pd.get_dummies(
        featured[
            [
                "store_id",
                "product_id",
                "category",
                "price",
                "promotion_flag",
                "day_of_week",
                "lag_1_units",
                "rolling_3_units",
            ]
        ],
        columns=["store_id", "product_id", "category"],
        drop_first=False,
    )
    output = featured.copy()
    output["forecast_units"] = model.predict(scoring_frame).round(0).astype(int)
    output["forecast_delta"] = output["forecast_units"] - output["units_sold"]
    output["inventory_action"] = output["forecast_delta"].apply(
        lambda value: "Increase replenishment" if value >= 3 else "Monitor current stock"
    )
    return output[
        [
            "date",
            "store_id",
            "product_id",
            "category",
            "units_sold",
            "forecast_units",
            "forecast_delta",
            "inventory_action",
        ]
    ]


def main() -> None:
    """Run the complete retail forecasting workflow."""
    sales = load_sales()
    featured = build_features(sales)
    model, mae = train_forecast_model(featured)
    output = create_forecast_output(featured, model)
    output.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved forecast output to {OUTPUT_PATH}")
    print(f"Validation MAE: {mae:.2f} units")


if __name__ == "__main__":
    main()
