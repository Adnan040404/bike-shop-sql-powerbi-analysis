-- Combines two years of hourly rider counts with per-rider price and cost,
-- then computes revenue and profit.
--
-- cost.COGS is a cost PER RIDER (it lines up with price, which is also per
-- rider), so it has to scale with volume the same way revenue does. An
-- earlier version of this query subtracted COGS once per row regardless of
-- how many riders were in that row -- that undercounted total cost by about
-- 97% and produced a 99.7% profit margin, which isn't a number a real
-- business would have. See verify_numbers.py for the full comparison.

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
    (riders * price) - (riders * COGS) AS profit   -- COGS scaled by riders, not a flat subtraction
FROM cte AS a
LEFT JOIN cost AS b
ON a.yr = b.yr;
