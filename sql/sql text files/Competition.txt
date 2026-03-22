-- 🚀 ✅ 1) List all competitions with their category name
SELECT 
    c.competition_id,
    c.competition_name,
    c.type,
    c.gender,
    cat.category_name
FROM sports_db.competitions c
INNER JOIN sports_db.categories cat
ON c.category_id = cat.category_id;

-- 🚀 ✅ 2) Count number of competitions in each category
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM sports_db.categories cat
LEFT JOIN sports_db.competitions c
ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_competitions DESC;


-- 🚀 ✅ 3) Find all competitions of type 'doubles'
SELECT 
    competition_id,
    competition_name,
    type,
    gender
FROM sports_db.competitions
WHERE type = 'doubles';

-- 🚀 ✅ 4) Get competitions for a specific category (e.g., ITF Men)
SELECT 
    c.competition_id,
    c.competition_name,
    c.type,
    c.gender
FROM sports_db.competitions c
INNER JOIN sports_db.categories cat
ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 🚀 ✅ 5) Identify parent competitions and sub-competitions
SELECT 
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM sports_db.competitions child
JOIN sports_db.competitions parent
ON child.parent_id = parent.competition_id;

-- 🚀 ✅ 6) Distribution of competition types by category
SELECT 
    cat.category_name,
    c.type,
    COUNT(*) AS total
FROM sports_db.competitions c
JOIN sports_db.categories cat
ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, total DESC;

-- 🚀 ✅ 7) List top-level competitions (no parent)
SELECT 
    competition_id,
    competition_name,
    type,
    gender
FROM sports_db.competitions
WHERE parent_id IS NULL;