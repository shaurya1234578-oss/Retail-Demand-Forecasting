/*
Project: Retail Demand Forecasting
Author: Shaurya Rajput
Date: 2026-06-29
Description: Relational schema for M5-style retail sales, product, store, and calendar dimensions.
*/

CREATE TABLE store_dim (
    store_id VARCHAR(20) PRIMARY KEY,
    city VARCHAR(80) NOT NULL,
    region VARCHAR(80) NOT NULL
);

CREATE TABLE product_dim (
    product_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(80) NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE calendar_dim (
    date_key DATE PRIMARY KEY,
    day_of_week INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    snap_flag INTEGER NOT NULL
);

CREATE TABLE sales_fact (
    sales_id BIGINT PRIMARY KEY,
    date_key DATE NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    units_sold INTEGER NOT NULL,
    sell_price DECIMAL(10, 2) NOT NULL,
    promotion_flag INTEGER NOT NULL,
    revenue DECIMAL(14, 2) NOT NULL,
    CONSTRAINT fk_sales_calendar FOREIGN KEY (date_key) REFERENCES calendar_dim(date_key),
    CONSTRAINT fk_sales_store FOREIGN KEY (store_id) REFERENCES store_dim(store_id),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES product_dim(product_id)
);

CREATE INDEX idx_sales_fact_date_store ON sales_fact (date_key, store_id);
CREATE INDEX idx_sales_fact_product_date ON sales_fact (product_id, date_key);

-- Query 1: Business-purpose verification query to confirm core warehouse tables are present after schema deployment.
WITH expected_tables AS (
    SELECT 'store_dim' AS table_name
    UNION ALL SELECT 'product_dim'
    UNION ALL SELECT 'calendar_dim'
    UNION ALL SELECT 'sales_fact'
), table_audit AS (
    SELECT
        expected_tables.table_name,
        ROW_NUMBER() OVER (ORDER BY expected_tables.table_name) AS audit_rank
    FROM expected_tables
)
SELECT table_name, audit_rank
FROM table_audit;
