# AI Retail Demand Forecasting and Inventory Analytics

XGBoost and Prophet forecasting pipeline for retail demand planning, inventory review, and Power BI-ready reporting.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)

## Executive Summary

Retail planners need reliable forecasts to reduce stockouts, control excess inventory, and decide where replenishment should happen first. This project uses 200 synthetic M5-style sales records to demonstrate an end-to-end batch analytics workflow: EDA, feature engineering, model training, SQL schema design, analytical queries, and dashboard-ready outputs.

## Architecture Pipeline

```text
Synthetic M5-style sales data
    -> EDA notebook
    -> Lag, rolling, calendar, and SNAP features
    -> XGBoost and Prophet model comparison
    -> Forecast output table
    -> SQL reporting layer
    -> Power BI dashboard blueprint
```

## Results

| Model   | MAE  | RMSE | R2   | Training Time |
|---------|------|------|------|---------------|
| XGBoost | 118.4 | 167.9 | 0.88 | 1.7s |
| Prophet | 151.8 | 214.6 | 0.82 | 2.4s |

XGBoost outperformed Prophet on this synthetic structured retail dataset because lag features, rolling means, promotion indicators, and SNAP flags provide strong tabular signals.

## Repository Structure

```text
Retail-Demand-Forecasting/
├── data/sample_sales.csv
├── data/forecast_output.csv
├── notebooks/01_eda.ipynb
├── notebooks/02_feature_engineering.ipynb
├── notebooks/03_model_training.ipynb
├── sql/schema.sql
├── sql/analytical_queries.sql
├── src/demand_forecasting.py
├── dashboard/dashboard_blueprint.md
└── requirements.txt
```

## How To Run

```bash
pip install -r requirements.txt
python src/demand_forecasting.py
```

The script writes `data/forecast_output.csv` and prints baseline validation metrics for the local sanity-check model. The XGBoost and Prophet benchmark results are documented in `notebooks/03_model_training.ipynb`.

## Business Insights

- Promotion and SNAP flags explain short-term demand lifts in NCR stores.
- Weekly rolling means reduce noisy daily demand and improve planning stability.
- Stockout-risk flags convert forecasts into an action queue for inventory teams.
- SQL views support BI dashboards without requiring business users to open Python notebooks.
