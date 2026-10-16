
import json
import logging
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load the token from the root .env file
load_dotenv(PROJECT_ROOT / ".env")
TMDB_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

if not TMDB_TOKEN:
    raise ValueError(
        "TMDB_BEARER_TOKEN is missing. Check the root .env file."
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

BASE_URL = "https://api.themoviedb.org/3"

MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536,
    597, 135397, 420818, 24428, 168259,
    99861, 284054, 12445, 181808, 330457,
    351286, 109445, 321612, 260513,
]

HEADERS = {
    "Authorization": f"Bearer {TMDB_TOKEN}",
    "accept": "application/json",
}


def fetch_endpoint(endpoint):
    """Fetch JSON data from a TMDB endpoint."""
    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30,
            )

            if response.status_code == 404:
                logging.warning("Not found: %s", endpoint)
                return None

            if response.status_code == 429:
                wait_seconds = 2 ** attempt
                logging.warning(
                    "Rate limited. Waiting %s seconds.",
                    wait_seconds,
                )
                time.sleep(wait_seconds)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            logging.warning(
                "Attempt %s failed for %s: %s",
                attempt + 1,
                endpoint,
                error,
            )

            if attempt < 2:
                time.sleep(2 ** attempt)

    logging.error("Giving up on endpoint: %s", endpoint)
    return None


def main():
    """Fetch movie details and credits for all supplied IDs."""
    movies = []
    failures = []

    for movie_id in MOVIE_IDS:
        logging.info(
            "Fetching movie %s (%s total IDs)",
            movie_id,
            len(MOVIE_IDS),
        )

        details = fetch_endpoint(f"movie/{movie_id}")

        if details is None:
            failures.append({
                "movie_id": movie_id,
                "endpoint": "details",
            })
            continue

        credits = fetch_endpoint(f"movie/{movie_id}/credits")

        if credits is None:
            failures.append({
                "movie_id": movie_id,
                "endpoint": "credits",
            })
            credits = {}

        # Keep the original API responses for traceability.
        movie_record = {
            "details": details,
            "credits": credits,
        }
        movies.append(movie_record)

        # Brief pause between movies to reduce request pressure.
        time.sleep(0.25)

    raw_file = RAW_DATA_DIR / "tmdb_movies_raw.json"
    with raw_file.open("w", encoding="utf-8") as file:
        json.dump(movies, file, indent=2, ensure_ascii=False)

    failure_file = RAW_DATA_DIR / "fetch_failures.json"
    with failure_file.open("w", encoding="utf-8") as file:
        json.dump(failures, file, indent=2, ensure_ascii=False)

    logging.info("Successfully fetched %s movie records.", len(movies))
    logging.info("Failed requests recorded: %s", len(failures))
    logging.info("Raw data saved to: %s", raw_file)
    logging.info("Failure log saved to: %s", failure_file)


if __name__ == "__main__":
    main()
