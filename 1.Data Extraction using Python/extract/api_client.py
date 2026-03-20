import requests
import logging
from config import COMPETITION_API_CONFIG,COMPLEX_API_CONFIG,RANKING_API_CONFIG,HEADERS

def fetch_competition():
    try:
        response = requests.get(COMPETITION_API_CONFIG["base_url"], headers=HEADERS)
        response.raise_for_status()

        logging.info("COMPETITION API call successful.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise

def fetch_complexes():
    try:
        response = requests.get(COMPLEX_API_CONFIG["base_url"], headers=HEADERS)
        response.raise_for_status()

        logging.info("COMPLEX API call successful.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise

def fetch_ranking():
    try:
        response = requests.get(RANKING_API_CONFIG["base_url"], headers=HEADERS)
        response.raise_for_status()

        logging.info("RANKING API call successful.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise