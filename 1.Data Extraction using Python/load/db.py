import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG,DATABASE_NAME
import logging

def get_connection():
    try:
        ensure_database_exists()

        connection = mysql.connector.connect(**DB_CONFIG)

        cursor = connection.cursor()
        
        create_category_competition_tables(cursor)
        create_category_competition_indexes(cursor)

        complex_create_tables(cursor)
        complex_create_indexes(cursor)

        create_competitor_tables(cursor)
        create_competitor_indexes(cursor)

        connection.commit()

        return connection

    except Error as err:
        logging.error(f"Database connection failed: {err}")
        raise


def ensure_database_exists():
    try:
        # ---- Remove database from config temporarily ----
        temp_config = DB_CONFIG.copy()
        temp_config.pop("database", None)

        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} "
            "DEFAULT CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci;"
        )

        cursor.close()
        connection.close()

        logging.info(f"Database '{DATABASE_NAME}' is ready.")

    except Error as err:
        logging.error(f"Database creation failed: {err}")
        raise

def create_category_competition_tables(cursor):
    """
    Creates tables:
    1. categories
    2. competitions
    """

    # ==============================
    # Categories Table
    # ==============================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id VARCHAR(50) PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
        )
    """)

    # ==============================
    # Competitions Table
    # ==============================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id VARCHAR(50) PRIMARY KEY,
            competition_name VARCHAR(100) NOT NULL,
            parent_id VARCHAR(50) NULL,
            type VARCHAR(20) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            category_id VARCHAR(50),
            CONSTRAINT fk_category
                FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
                ON DELETE CASCADE
        )
    """)

    logging.info("Categories and Competitions tables ensured.")

def create_category_competition_indexes(cursor):
    """
    Creates indexes safely (avoids duplicate index error 1061).
    """

    try:
        cursor.execute("CREATE INDEX idx_comp_category ON competitions(category_id)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_comp_gender ON competitions(gender)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_comp_type ON competitions(type)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_parent ON competitions(parent_id)")
    except Error as e:
        if e.errno != 1061:
            raise

    logging.info("Competition indexes ensured.")

def complex_create_tables(cursor):
    """
    Creates tables according to required schema:
    1. complexes
    2. venues
    """

    # Complexes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complexes (
            complex_id VARCHAR(50) PRIMARY KEY,
            complex_name VARCHAR(100) NOT NULL
        )
    """)

    # Venues Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            venue_id VARCHAR(50) PRIMARY KEY,
            venue_name VARCHAR(100) NOT NULL,
            city_name VARCHAR(100) NOT NULL,
            country_name VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL,
            timezone VARCHAR(100) NOT NULL,
            complex_id VARCHAR(50),
            CONSTRAINT fk_complex
                FOREIGN KEY (complex_id)
                REFERENCES complexes(complex_id)
                ON DELETE CASCADE
        )
    """)

    logging.info("Tables ensured.")


def complex_create_indexes(cursor):
    """
    Creates indexes safely (avoids duplicate index error 1061).
    """

    try:
        cursor.execute("CREATE INDEX idx_city ON venues(city_name)")
    except Error as e:
        if e.errno != 1061:  # Duplicate key name
            raise

    try:
        cursor.execute("CREATE INDEX idx_country ON venues(country_code)")
    except Error as e:
        if e.errno != 1061:
            raise

    logging.info("Indexes ensured.")

def create_competitor_tables(cursor):
    """
    Creates tables:
    1. competitors
    2. competitor_rankings
    """

    # ==============================
    # Competitors Table
    # ==============================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            competitor_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL,
            abbreviation VARCHAR(10) NOT NULL
        )
    """)

    # ==============================
    # Competitor Rankings Table
    # ==============================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitor_rankings (
            rank_id INT AUTO_INCREMENT PRIMARY KEY,
            ranking INT NOT NULL,
            movement INT NOT NULL,
            points INT NOT NULL,
            competitions_played INT NOT NULL,
            competitor_id VARCHAR(50),
            CONSTRAINT fk_competitor
                FOREIGN KEY (competitor_id)
                REFERENCES competitors(competitor_id)
                ON DELETE CASCADE
        )
    """)

    logging.info("Competitor tables ensured.")

def create_competitor_indexes(cursor):
    """
    Creates indexes safely (avoids duplicate index error 1061).
    """

    try:
        cursor.execute("CREATE INDEX idx_ranking ON competitor_rankings(ranking)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_points ON competitor_rankings(points)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_competitor_id ON competitor_rankings(competitor_id)")
    except Error as e:
        if e.errno != 1061:
            raise

    try:
        cursor.execute("CREATE INDEX idx_country ON competitors(country_code)")
    except Error as e:
        if e.errno != 1061:
            raise

    logging.info("Competitor indexes ensured.")