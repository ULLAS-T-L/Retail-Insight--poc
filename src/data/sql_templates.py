"""
sql_templates.py

This module contains parameterized SQL templates for the 4 core intents. Safe SQLite 
named parameters (e.g. :brand, :region) are used to prevent SQL injection. Arbitrary 
SQL string generation/concatenation is avoided.

Service Layer Usage:
The service layer (api/routes.py or a dedicated agent service) should load the 
appropriate template from here, construct a dictionary of bindings corresponding 
to the requested parameters, and execute it using sqlite3 logic: 
    >>> cursor.execute(SQL_TEMPLATES["kpi_timeseries"], params_dict)
"""

# 1. kpi_timeseries
# Used to analyze the trend of units and net_sales over time for a given slice 
# (brand, region, channel) within a specific date range.
KPI_TIMESERIES = """
SELECT 
    f.date,
    SUM(f.net_sales) as total_net_sales,
    SUM(f.units) as total_units
FROM fact_sellout f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_retailer r ON f.retailer_id = r.retailer_id
WHERE 
    p.brand = :brand AND
    f.region = :region AND
    r.channel = :channel AND
    f.date >= :start_date AND f.date <= :end_date
GROUP BY 
    f.date
ORDER BY 
    f.date ASC;
"""

# 2. compare_periods
# Used to compare performance metrics between two distinct time periods.
# Employs conditional grouping to map dates into either 'Period 1' or 'Period 2'.
COMPARE_PERIODS = """
SELECT
    CASE 
        WHEN f.date >= :period_1_start AND f.date <= :period_1_end THEN 'Period 1'
        WHEN f.date >= :period_2_start AND f.date <= :period_2_end THEN 'Period 2'
    END AS period_name,
    SUM(f.net_sales) as total_net_sales,
    SUM(f.units) as total_units
FROM fact_sellout f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_retailer r ON f.retailer_id = r.retailer_id
WHERE 
    p.brand = :brand AND
    f.region = :region AND
    r.channel = :channel AND
    ((f.date >= :period_1_start AND f.date <= :period_1_end) OR 
     (f.date >= :period_2_start AND f.date <= :period_2_end))
GROUP BY 
    period_name
ORDER BY 
    period_name ASC;
"""

# 3. kpi_drivers
# Used to analyze the underlying drivers (distribution, price, promo) of sales. 
# Fetches granular aggregated metrics to correlate drivers against sales performance.
KPI_DRIVERS = """
SELECT 
    f.date,
    p.product_id,
    f.distribution,
    f.price_index,
    f.promo_flag,
    SUM(f.units) as units,
    SUM(f.net_sales) as net_sales
FROM fact_sellout f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_retailer r ON f.retailer_id = r.retailer_id
WHERE 
    p.brand = :brand AND
    f.region = :region AND
    r.channel = :channel AND
    f.date >= :start_date AND f.date <= :end_date
GROUP BY 
    f.date, p.product_id, f.distribution, f.price_index, f.promo_flag
ORDER BY 
    f.date ASC;
"""

# 4. compliance_check
# Used to verify if brand performance meets certain structural core threshold limits 
# Checks if the computed market share or distribution drops below given thresholds.
COMPLIANCE_CHECK = """
WITH TotalMarket AS (
    SELECT 
        f.date,
        SUM(f.net_sales) as market_total_sales
    FROM fact_sellout f
    JOIN dim_retailer r ON f.retailer_id = r.retailer_id
    WHERE 
        f.region = :region AND
        r.channel = :channel AND
        f.date >= :start_date AND f.date <= :end_date
    GROUP BY f.date
),
BrandSales AS (
    SELECT 
        f.date,
        f.product_id,
        AVG(f.distribution) as avg_distribution,
        SUM(f.net_sales) as total_net_sales
    FROM fact_sellout f
    JOIN dim_product p ON f.product_id = p.product_id
    JOIN dim_retailer r ON f.retailer_id = r.retailer_id
    WHERE 
        p.brand = :brand AND
        f.region = :region AND
        r.channel = :channel AND
        f.date >= :start_date AND f.date <= :end_date
    GROUP BY f.date, f.product_id
)
SELECT 
    b.date,
    b.product_id,
    b.total_net_sales,
    m.market_total_sales,
    (b.total_net_sales / CAST(m.market_total_sales AS REAL)) as market_share,
    b.avg_distribution
FROM BrandSales b
JOIN TotalMarket m ON b.date = m.date
WHERE 
    (b.total_net_sales / CAST(m.market_total_sales AS REAL)) < :market_share_threshold OR 
    b.avg_distribution < :distribution_threshold;
"""

# Export mapping index
SQL_TEMPLATES = {
    "kpi_timeseries": KPI_TIMESERIES,
    "compare_periods": COMPARE_PERIODS,
    "kpi_drivers": KPI_DRIVERS,
    "compliance_check": COMPLIANCE_CHECK
}
