import logging
from extract.extractor import extract_competition,extract_complexes,extract_ranking
from transform.transformer import competition_transform_data,complex_transform_data,ranking_transform_data
from load.db import create_category_competition_indexes, create_category_competition_tables, create_competitor_indexes, create_competitor_tables, get_connection, complex_create_tables, complex_create_indexes
from load.loader import load_complexes, load_venues,load_categories,load_competitions,load_competitors,load_rankings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():
    connection = None
    cursor = None

    try:
        # ==============================
        # EXTRACT
        # ==============================
        competition_raw_data = extract_competition()
        complexes_raw_data = extract_complexes()
        ranking_raw_data = extract_ranking()

        logging.info("Data extracted successfully")

        # ==============================
        # TRANSFORM
        # ==============================
        categories, competitions = competition_transform_data(competition_raw_data)
        complexes, venues = complex_transform_data(complexes_raw_data)
        competitors, rankings = ranking_transform_data(ranking_raw_data)

        logging.info("Data transformed successfully")

        # ==============================
        # LOAD
        # ==============================
        connection = get_connection()
        cursor = connection.cursor()

        # Create Tables
        create_category_competition_tables(cursor)
        create_category_competition_indexes(cursor)

        complex_create_tables(cursor)
        complex_create_indexes(cursor)

        create_competitor_tables(cursor)
        create_competitor_indexes(cursor)

        # Insert Data (ORDER MATTERS)
        load_categories(cursor, categories)
        load_competitions(cursor, competitions)

        load_complexes(cursor, complexes)
        load_venues(cursor, venues)
       
        load_competitors(cursor, competitors)
        load_rankings(cursor, rankings)

        connection.commit()

        logging.info("✅ ETL completed successfully")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")

        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
            logging.info("Database connection closed")
            
if __name__ == "__main__":
    run_pipeline()