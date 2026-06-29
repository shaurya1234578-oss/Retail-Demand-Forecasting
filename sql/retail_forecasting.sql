/*
Project: Retail Demand Forecasting
Author: Shaurya Rajput
Date: 2026-06-29
Description: Dashboard-ready SQL views for forecast accuracy, replenishment priority, and product-store demand monitoring.
*/

-- Query 1: Create a reporting table for actual versus forecasted demand.
CREATE TABLE forecast_output (
    forecast_date DATE,
    store_id VARCHAR(20),
    product_id VARCHAR(20),
    category VARCHAR(80),
    units_sold INTEGER,
    forecast_units INTEGER,
    forecast_error INTEGER,
    stockout_risk_flag INTEGER
);

-- Query 2: Summarize forecast accuracy by store and product for dashboard monitoring.
WITH forecast_accuracy AS (
    SELECT
        store_id,
        product_id,
        category,
        COUNT(*) AS forecast_days,
        AVG(ABS(forecast_error)) AS mean_absolute_error,
        SUM(units_sold) AS actual_units,
        SUM(forecast_units) AS forecast_units
    FROM forecast_output
    GROUP BY store_id, product_id, category
)
SELECT
    store_id,
    product_id,
    category,
    forecast_days,
    mean_absolute_error,
    actual_units,
    forecast_units,
    RANK() OVER (ORDER BY mean_absolute_error DESC) AS error_rank
FROM forecast_accuracy;

-- Query 3: Build a replenishment action queue from stockout-risk forecast rows.
WITH replenishment_queue AS (
    SELECT
        forecast_date,
        store_id,
        product_id,
        category,
        forecast_units - units_sold AS demand_gap,
        stockout_risk_flag
    FROM forecast_output
    WHERE stockout_risk_flag = 1
)
SELECT
    forecast_date,
    store_id,
    product_id,
    category,
    demand_gap,
    ROW_NUMBER() OVER (ORDER BY demand_gap DESC) AS replenishment_rank
FROM replenishment_queue;
