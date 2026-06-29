/*
Project: Retail Demand Forecasting
Author: Shaurya Rajput
Date: 2026-06-29
Description: Analytical SQL for demand forecasting, seasonality, stockout risk, and store performance.
*/

-- Query 1: Identify top products by revenue for category-level merchandising focus.
WITH product_revenue AS (
    SELECT
        product_dim.product_id,
        product_dim.category,
        SUM(sales_fact.revenue) AS total_revenue,
        RANK() OVER (ORDER BY SUM(sales_fact.revenue) DESC) AS revenue_rank
    FROM sales_fact
    INNER JOIN product_dim ON sales_fact.product_id = product_dim.product_id
    GROUP BY product_dim.product_id, product_dim.category
)
SELECT product_id, category, total_revenue, revenue_rank
FROM product_revenue
WHERE revenue_rank <= 10;

-- Query 2: Track weekly sales trend and week-over-week movement.
WITH weekly_sales AS (
    SELECT
        calendar_dim.week_of_year,
        SUM(sales_fact.units_sold) AS weekly_units,
        LAG(SUM(sales_fact.units_sold)) OVER (ORDER BY calendar_dim.week_of_year) AS previous_week_units
    FROM sales_fact
    INNER JOIN calendar_dim ON sales_fact.date_key = calendar_dim.date_key
    GROUP BY calendar_dim.week_of_year
)
SELECT
    week_of_year,
    weekly_units,
    previous_week_units,
    weekly_units - COALESCE(previous_week_units, weekly_units) AS unit_change
FROM weekly_sales;

-- Query 3: Flag stockout risk where recent product demand is materially above historical average.
WITH product_daily AS (
    SELECT
        sales_fact.product_id,
        sales_fact.date_key,
        SUM(sales_fact.units_sold) AS daily_units
    FROM sales_fact
    GROUP BY sales_fact.product_id, sales_fact.date_key
), rolling_demand AS (
    SELECT
        product_id,
        date_key,
        daily_units,
        AVG(daily_units) OVER (PARTITION BY product_id ORDER BY date_key ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7_day_units
    FROM product_daily
)
SELECT product_id, date_key, daily_units, rolling_7_day_units,
       CASE WHEN daily_units > rolling_7_day_units * 1.20 THEN 'Stockout Risk' ELSE 'Normal' END AS risk_flag
FROM rolling_demand;

-- Query 4: Calculate seasonality index by month against overall average demand.
WITH monthly_demand AS (
    SELECT calendar_dim.month_number, AVG(sales_fact.units_sold) AS avg_monthly_units
    FROM sales_fact
    INNER JOIN calendar_dim ON sales_fact.date_key = calendar_dim.date_key
    GROUP BY calendar_dim.month_number
), overall_demand AS (
    SELECT AVG(units_sold) AS avg_units FROM sales_fact
)
SELECT
    monthly_demand.month_number,
    monthly_demand.avg_monthly_units,
    monthly_demand.avg_monthly_units / overall_demand.avg_units AS seasonality_index
FROM monthly_demand
CROSS JOIN overall_demand;

-- Query 5: Compare store performance and rank stores by revenue productivity.
WITH store_performance AS (
    SELECT
        store_dim.store_id,
        store_dim.city,
        SUM(sales_fact.revenue) AS revenue,
        SUM(sales_fact.units_sold) AS units,
        ROW_NUMBER() OVER (ORDER BY SUM(sales_fact.revenue) DESC) AS store_rank
    FROM sales_fact
    INNER JOIN store_dim ON sales_fact.store_id = store_dim.store_id
    GROUP BY store_dim.store_id, store_dim.city
)
SELECT store_id, city, revenue, units, store_rank
FROM store_performance;
