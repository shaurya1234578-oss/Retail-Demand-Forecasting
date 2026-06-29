-- Retail demand forecasting reporting queries.

CREATE TABLE forecast_output (
    forecast_date DATE,
    store_id VARCHAR(20),
    product_id VARCHAR(20),
    category VARCHAR(80),
    units_sold INTEGER,
    forecast_units INTEGER,
    forecast_delta INTEGER,
    inventory_action VARCHAR(80)
);

CREATE VIEW forecast_accuracy_summary AS
SELECT
    store_id,
    product_id,
    category,
    COUNT(*) AS forecast_days,
    AVG(ABS(forecast_delta)) AS mean_absolute_error,
    SUM(units_sold) AS actual_units,
    SUM(forecast_units) AS forecast_units
FROM forecast_output
GROUP BY store_id, product_id, category;

SELECT
    store_id,
    product_id,
    category,
    forecast_date,
    units_sold,
    forecast_units,
    forecast_delta,
    inventory_action
FROM forecast_output
WHERE inventory_action = 'Increase replenishment'
ORDER BY forecast_delta DESC;
