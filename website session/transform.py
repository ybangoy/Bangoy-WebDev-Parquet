import duckdb

duckdb.sql("""
    COPY (
        SELECT DISTINCT
        
            --- trim
            TRIM(session_id) AS session_id,
            session_date,
            customer_id,
            store_id,
            TRIM(device_type) as device_type,
            
            --- split
            SPLIT_PART(browser_os, '|', 1) AS browser,
            SPLIT_PART(browser_os, '|', 2) AS os,
            
            --- concat
            CONCAT(customer_id, ' ', store_id) AS customer_store_id,           
            
            --- missing values (coalesce)
            session_purchase_made,
            session_duration_minutes,
            session_pages_visited,
            COALESCE(session_quality_score, avg(session_quality_score) OVER()) AS session_quality_score,


        FROM 'bronze.parquet'
    )
    TO 'silver.parquet'
    (FORMAT PARQUET);
""")
