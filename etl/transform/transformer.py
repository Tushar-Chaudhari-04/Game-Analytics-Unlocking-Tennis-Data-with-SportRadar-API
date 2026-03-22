import logging

def competition_transform_data(raw_data):
    """
    Transforms raw API JSON into structured data
    for categories and competitions tables.
    """

    categories = []
    competitions = []

    seen_category_ids = set()
    seen_competition_ids = set()

    try:
        for comp in raw_data.get("competitions", []):

            # ==============================
            # CATEGORY EXTRACTION
            # ==============================
            category = comp.get("category", {})

            category_id = category.get("id")
            category_name = category.get("name")

            # Validate category
            if category_id and category_name:
                if category_id not in seen_category_ids:
                    categories.append({
                        "category_id": category_id,
                        "category_name": category_name
                    })
                    seen_category_ids.add(category_id)
            else:
                logging.warning("Skipping category due to missing fields.")

            # ==============================
            # COMPETITION EXTRACTION
            # ==============================
            competition_id = comp.get("id")
            competition_name = comp.get("name")
            parent_id = comp.get("parent_id")  # can be None
            comp_type = comp.get("type")
            gender = comp.get("gender")

            # Validate NOT NULL fields
            if not all([
                competition_id,
                competition_name,
                comp_type,
                gender
            ]):
                logging.warning(
                    f"Skipping competition due to missing fields: {competition_id}"
                )
                continue

            # Avoid duplicates
            if competition_id in seen_competition_ids:
                continue

            competitions.append({
                "competition_id": competition_id,
                "competition_name": competition_name,
                "parent_id": parent_id,
                "type": comp_type,
                "gender": gender,
                "category_id": category_id
            })

            seen_competition_ids.add(competition_id)

        logging.info(
            f"Transformation complete: {len(categories)} categories, {len(competitions)} competitions"
        )

        return categories, competitions

    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        return [], []
    
def complex_transform_data(raw_data):
    """
    Transforms raw API JSON into structured data
    matching the database schema.
    """

    complexes = []
    venues = []

    for complex_obj in raw_data.get("complexes", []):

        complex_id = complex_obj.get("id")
        complex_name = complex_obj.get("name")

        if not complex_id or not complex_name:
            logging.warning("Skipping complex due to missing id or name.")
            continue

        complexes.append({
            "complex_id": complex_id,
            "complex_name": complex_name
        })

        for venue in complex_obj.get("venues", []):

            venue_id = venue.get("id")
            venue_name = venue.get("name")
            city_name = venue.get("city_name")
            country_name = venue.get("country_name")
            country_code = venue.get("country_code")
            timezone = venue.get("timezone")

            # Validate required NOT NULL fields
            if not all([
                venue_id,
                venue_name,
                city_name,
                country_name,
                country_code,
                timezone
            ]):
                logging.warning(
                    f"Skipping venue under complex {complex_id} due to missing fields."
                )
                continue

            venues.append({
                "venue_id": venue_id,
                "venue_name": venue_name,
                "city_name": city_name,
                "country_name": country_name,
                "country_code": country_code,
                "timezone": timezone,
                "complex_id": complex_id
            })

    logging.info("Transformation completed successfully.")
    return complexes, venues


import logging

def ranking_transform_data(raw_data):
    """
    Transforms API JSON into:
    1. competitors table data
    2. competitor_rankings table data
    """

    competitors = []
    rankings = []

    seen_competitors = set()

    for ranking_block in raw_data.get("rankings", []):

        for item in ranking_block.get("competitor_rankings", []):

            # ==============================
            # COMPETITOR
            # ==============================
            comp = item.get("competitor", {})

            competitor_id = comp.get("id")
            name = comp.get("name")
            country = comp.get("country")
            country_code = comp.get("country_code")
            abbreviation = comp.get("abbreviation")

            # Validate
            if not all([competitor_id, name, country, country_code, abbreviation]):
                logging.warning("Skipping competitor due to missing fields.")
                continue

            # Deduplication
            if competitor_id not in seen_competitors:
                competitors.append({
                    "competitor_id": competitor_id,
                    "name": name,
                    "country": country,
                    "country_code": country_code,
                    "abbreviation": abbreviation
                })
                seen_competitors.add(competitor_id)

            # ==============================
            # RANKING
            # ==============================
            ranking = item.get("rank")   # renamed
            movement = item.get("movement")
            points = item.get("points")
            competitions_played = item.get("competitions_played")

            if not all([
                ranking is not None,
                movement is not None,
                points is not None,
                competitions_played is not None
            ]):
                logging.warning(f"Skipping ranking for {competitor_id}")
                continue

            rankings.append({
                "ranking": ranking,  # IMPORTANT (not 'rank')
                "movement": movement,
                "points": points,
                "competitions_played": competitions_played,
                "competitor_id": competitor_id
            })

    logging.info("Transformation completed successfully.")
    return competitors, rankings