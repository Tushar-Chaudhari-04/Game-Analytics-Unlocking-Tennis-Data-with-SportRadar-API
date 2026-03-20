-- Execute the following SQL queries:

-- 1) List all venues along with their associated complex name
      select v.venue_name,c.complex_name from sports_db.venues as v
      join sports_db.complexes as c 
      on v.complex_id=c.complex_id;
      
-- 2) Count the number of venues in each complex
        SELECT 
			c.complex_name,
			COUNT(v.venue_id) AS total_venues
		FROM sports_db.complexes c
		LEFT JOIN sports_db.venues v
		ON c.complex_id = v.complex_id
		GROUP BY c.complex_name;
       
-- 3) Get details of venues in a specific country (e.g., Chile)
select * from sports_db.venues as v where v.country_name="Chile";

-- 4) Identify all venues and their timezones
    select v.venue_name,v.timezone from sports_db.venues v;
    
-- 5) Find complexes that have more than one venue
	select c.complex_name,COUNT(v.venue_id) as total_venues
    from sports_db.complexes as c
    JOIN sports_db.venues v
    where c.complex_id=v.complex_id
    group by c.complex_name
    having count(v.venue_id)>1;
    
-- 6) List venues grouped by country
select v.country_name,count(v.venue_id) as total_venues from sports_db.venues as v group by v.country_name;

-- 7) Find all venues for a specific complex (e.g., Nacional)
      select v.venue_name,v.city_name,c.complex_name from sports_db.venues as v
      inner join sports_db.complexes as c 
      on v.complex_id=c.complex_id
      where c.complex_name="Nacional";