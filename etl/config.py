"""
Application configuration file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_NAME = os.getenv("DB_NAME")
API_KEY=os.getenv("API_KEY")

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}


DB_CONFIG = {
    "host": HOST,
    "user": USER,
    "password": PASSWORD,
    "database":DATABASE_NAME
}

COMPETITION_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/competitions.json",
    "api-key": API_KEY,
    "accept": "application/json",
}

COMPLEX_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/complexes.json",
    "api-key": API_KEY,
    "accept": "application/json",
}

RANKING_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json",
    "api-key": API_KEY,
    "accept": "application/json",
}