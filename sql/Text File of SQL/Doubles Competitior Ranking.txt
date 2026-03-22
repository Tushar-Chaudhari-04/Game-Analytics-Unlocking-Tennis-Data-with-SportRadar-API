
-- Query 1: Get all competitors with their rank and points
SELECT 
    c.competitor_id,
    c.name,
    c.country,
    c.country_code,
    dr.ranking,
    dr.points,
    dr.movement,
    dr.competitions_played
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
ORDER BY dr.ranking ASC;

-- Query 2: Find competitors ranked in the top 5
SELECT 
    c.competitor_id,
    c.name,
    c.country,
    dr.ranking,
    dr.points,
    dr.movement
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
WHERE dr.ranking <= 5
ORDER BY dr.ranking ASC;

-- Query 3: List competitors with no rank movement (stable rank)
SELECT 
    c.competitor_id,
    c.name,
    c.country,
    dr.ranking,
    dr.points,
    dr.movement
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
WHERE dr.movement = 0
ORDER BY dr.ranking ASC;

-- Query 4: Get the total points of competitors from a specific country (e.g., Croatia)
SELECT 
    c.country,
    c.country_code,
    SUM(dr.points) AS total_points,
    COUNT(c.competitor_id) AS number_of_competitors,
    AVG(dr.points) AS average_points
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country, c.country_code;

-- Query 5: Count the number of competitors per country
SELECT 
    c.country,
    c.country_code,
    COUNT(c.competitor_id) AS competitor_count,
    SUM(dr.points) AS total_points,
    AVG(dr.points) AS average_points
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
GROUP BY c.country, c.country_code
ORDER BY competitor_count DESC, total_points DESC;

-- Query 6: Find competitors with the highest points in the current week
SELECT 
    c.competitor_id,
    c.name,
    c.country,
    c.country_code,
    dr.ranking,
    dr.points,
    dr.movement,
    dr.competitions_played
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
ORDER BY dr.points DESC
LIMIT 10;

-- ============================================================
-- SECTION 4: ADDITIONAL USEFUL QUERIES
-- ============================================================

-- Get competitors with positive movement (climbing ranks)
SELECT 
    c.name,
    c.country,
    dr.ranking,
    dr.movement,
    dr.points
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
WHERE dr.movement > 0
ORDER BY dr.movement DESC;

-- Get competitors with negative movement (dropping ranks)
SELECT 
    c.name,
    c.country,
    dr.ranking,
    dr.movement,
    dr.points
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
WHERE dr.movement < 0
ORDER BY dr.movement ASC;

-- Get average points by country (countries with multiple competitors)
SELECT 
    c.country,
    COUNT(*) AS competitor_count,
    AVG(dr.points) AS avg_points,
    MAX(dr.points) AS max_points,
    MIN(dr.points) AS min_points
FROM sports_db.competitors c
INNER JOIN sports_db.competitor_rankings dr ON c.competitor_id = dr.competitor_id
GROUP BY c.country
HAVING competitor_count > 1
ORDER BY avg_points DESC;
