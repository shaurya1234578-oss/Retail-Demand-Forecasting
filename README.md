# AI Retail Demand Forecasting and Inventory Analytics

An end-to-end retail analytics portfolio project for demand forecasting, inventory planning, and business intelligence reporting.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Forecasting](https://img.shields.io/badge/Forecasting-Retail%20Demand-success?style=flat-square)

## Executive Summary

Retail teams lose revenue when demand forecasts are inaccurate. Under-forecasting creates stockouts and missed sales, while over-forecasting increases inventory holding cost and markdown risk.

This project demonstrates a structured forecasting workflow that transforms sales history into demand features, baseline predictions, inventory recommendations, and dashboard-ready reporting tables.

## Business Problem

The goal is to support inventory planners with answers to practical questions:

- Which products are likely to face demand spikes?
- Which stores or categories need replenishment attention?
- Where is inventory risk caused by overstock or stockout patterns?
- How can forecasting output be translated into BI dashboards for business teams?

## Key Features

- Feature engineering for date, lag, rolling average, and store-product demand signals.
- Baseline forecasting workflow using Python and scikit-learn.
- SQL schema and analytical queries for BI reporting.
- Dashboard blueprint for Power BI or Tableau.
- Actionable inventory recommendations based on forecast movement.

## Architecture Pipeline

```text
Raw retail sales
    -> Data cleaning and validation
    -> Feature engineering
    -> Forecast model training
    -> Forecast and inventory recommendation output
    -> SQL reporting views
    -> BI dashboard and planning actions
```

## Repository Structure

```text
Retail-Demand-Forecasting/
├── data/
│   └── sample_sales.csv
├── dashboard/
│   └── dashboard_blueprint.md
├── docs/
│   └── inventory_insights.md
├── models/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── sql/
│   └── retail_forecasting.sql
├── src/
│   └── demand_forecasting.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Actionable Insights Demonstrated

- Products with rising rolling demand and high forecast variance should be reviewed before purchase orders are finalized.
- Store-category combinations with repeated under-forecasting need safety-stock adjustments.
- Slow-moving products should be flagged for markdown or inventory redistribution.
- Forecast dashboards should show demand trend, forecast error, stockout risk, and replenishment priority together.

## How To Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the forecasting workflow:

```bash
python src/demand_forecasting.py
```

3. Review the generated output:

```text
data/forecast_output.csv
```

4. Use `sql/retail_forecasting.sql` to create reporting tables and dashboard views.

## Dashboard Pages

- Executive Overview: sales, forecasted demand, forecast error, stockout risk.
- Product Performance: category, product, and store-level trends.
- Inventory Planning: replenishment priority and suggested business action.
- Forecast Monitoring: actual versus predicted demand.

## Future Enhancements

- Add full M5 Forecasting dataset workflow.
- Compare multiple models such as XGBoost, Prophet, and Random Forest.
- Add model tracking and scheduled retraining.
- Publish a Power BI dashboard screenshot and downloadable template.
- Deploy a forecasting API for real-time planning.

## Suggested GitHub Topics

`retail-analytics`, `demand-forecasting`, `inventory-optimization`, `machine-learning`, `time-series`, `business-intelligence`, `powerbi-dashboard`, `sql`, `python`, `pandas`, `scikit-learn`, `portfolio-project`

## Author

Shaurya Rajput  
Data Analytics | Business Intelligence | Applied Machine Learning
