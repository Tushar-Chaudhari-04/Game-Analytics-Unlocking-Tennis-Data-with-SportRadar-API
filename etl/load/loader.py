import logging


def load_categories(cursor, categories):
    """
    Loads data into categories table.
    Uses UPSERT to avoid duplicate primary key errors.
    """

    for c in categories:
        cursor.execute("""
            INSERT INTO categories (
                category_id,
                category_name
            )
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                category_name = VALUES(category_name)
        """, (
            c["category_id"],
            c["category_name"]
        ))

    logging.info("Categories loaded successfully.")
def load_competitions(cursor, competitions):
    """
    Loads data into competitions table.
    Uses UPSERT to avoid duplicate primary key errors.
    """

    for comp in competitions:
        cursor.execute("""
            INSERT INTO competitions (
                competition_id,
                competition_name,
                parent_id,
                type,
                gender,
                category_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                competition_name = VALUES(competition_name),
                parent_id = VALUES(parent_id),
                type = VALUES(type),
                gender = VALUES(gender),
                category_id = VALUES(category_id)
        """, (
            comp["competition_id"],
            comp["competition_name"],
            comp["parent_id"],
            comp["type"],
            comp["gender"],
            comp["category_id"]
        ))

    logging.info("Competitions loaded successfully.")

def load_complexes(cursor, complexes):
    """
    Loads data into complexes table.
    Uses UPSERT to avoid duplicate primary key errors.
    """

    for c in complexes:
        cursor.execute("""
            INSERT INTO complexes (
                complex_id,
                complex_name
            )
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                complex_name = VALUES(complex_name)
        """, (
            c["complex_id"],
            c["complex_name"]
        ))

    logging.info("Complexes loaded successfully.")


def load_venues(cursor, venues):
    """
    Loads data into venues table.
    Uses UPSERT to avoid duplicate primary key errors.
    """

    for v in venues:
        cursor.execute("""
            INSERT INTO venues (
                venue_id,
                venue_name,
                city_name,
                country_name,
                country_code,
                timezone,
                complex_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                venue_name = VALUES(venue_name),
                city_name = VALUES(city_name),
                country_name = VALUES(country_name),
                country_code = VALUES(country_code),
                timezone = VALUES(timezone),
                complex_id = VALUES(complex_id)
        """, (
            v["venue_id"],
            v["venue_name"],
            v["city_name"],
            v["country_name"],
            v["country_code"],
            v["timezone"],
            v["complex_id"]
        ))

    logging.info("Venues loaded successfully.")

def load_competitors(cursor, competitors):
    """
    Load data into competitors table
    """

    for c in competitors:
        cursor.execute("""
            INSERT INTO competitors (
                competitor_id,
                name,
                country,
                country_code,
                abbreviation
            )
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                country = VALUES(country),
                country_code = VALUES(country_code),
                abbreviation = VALUES(abbreviation)
        """, (
            c["competitor_id"],
            c["name"],
            c["country"],
            c["country_code"],
            c["abbreviation"]
        ))

    logging.info("Competitors loaded successfully.")

def load_rankings(cursor, rankings):
    """
    Load data into competitor_rankings table
    """

    for r in rankings:
        cursor.execute("""
            INSERT INTO competitor_rankings (
                ranking,
                movement,
                points,
                competitions_played,
                competitor_id
            )
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                ranking = VALUES(ranking),
                movement = VALUES(movement),
                points = VALUES(points),
                competitions_played = VALUES(competitions_played)
        """, (
            r["ranking"],
            r["movement"],
            r["points"],
            r["competitions_played"],
            r["competitor_id"]
        ))

    logging.info("Rankings loaded successfully.")