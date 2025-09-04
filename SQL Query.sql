
WITH cte AS (
    SELECT * FROM year_01
    UNION ALL
    SELECT * FROM year_02
)
SELECT 
    dteday, 
    season, 
    a.yr, 
    weekday, 
    hr, 
    rider_type, 
    riders, 
    price, 
    COGS,
    (riders * price) AS revenue,
    (riders * price - COGS) AS profit
FROM cte AS a
LEFT JOIN cost AS b 
ON a.yr = b.yr;


















