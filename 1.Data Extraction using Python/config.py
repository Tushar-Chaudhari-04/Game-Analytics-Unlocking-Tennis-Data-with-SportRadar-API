"""
Application configuration file.
"""

import os

DATABASE_NAME = "sports_db"

HEADERS = {
    "accept": "application/json",
    "x-api-key": "ZR78SfBxEPdAEfFzQxNJg1MXXVbtcGEqwnz6BPq8"
}


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@1234",
    "database":"sports_db"
}

COMPETITION_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/competitions.json",
    "api-key": "ZR78SfBxEPdAEfFzQxNJg1MXXVbtcGEqwnz6BPq8",
    "accept": "application/json",
}

COMPLEX_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/complexes.json",
    "api-key": "ZR78SfBxEPdAEfFzQxNJg1MXXVbtcGEqwnz6BPq8",
    "accept": "application/json",
}

RANKING_API_CONFIG = {
    "base_url":"https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json",
    "api-key": "ZR78SfBxEPdAEfFzQxNJg1MXXVbtcGEqwnz6BPq8",
    "accept": "application/json",
}