
import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TOKEN = os.getenv("TMDB_BEARER_TOKEN")

if not TOKEN:
    raise ValueError(
        "TMDB_BEARER_TOKEN was not found. Check your .env file."
    )

BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "accept": "application/json",
}

# TMDB person IDs
UMA_THURMAN_ID = 139
QUENTIN_TARANTINO_ID = 138


def get_json(url, params=None):
    """Send an authenticated GET request to TMDB."""
    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# Find movies associated with both people.
# We will verify the exact cast and director credits afterward.
candidates = []
page = 1

while True:
    data = get_json(
        f"{BASE_URL}/discover/movie",
        params={
            "with_cast": UMA_THURMAN_ID,
            "with_crew": QUENTIN_TARANTINO_ID,
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "language": "en-US",
            "page": page,
        },
    )

    candidates.extend(data.get("results", []))

    if page >= data.get("total_pages", 1):
        break

    page += 1

matches = []

for movie in candidates:
    movie_id = movie["id"]

    # Fetch full movie details, including runtime.
    details = get_json(f"{BASE_URL}/movie/{movie_id}")

    # Fetch cast and crew to verify credits.
    credits = get_json(f"{BASE_URL}/movie/{movie_id}/credits")

    uma_is_cast = any(
        person["id"] == UMA_THURMAN_ID
        for person in credits.get("cast", [])
    )

    tarantino_directed = any(
        person["id"] == QUENTIN_TARANTINO_ID
        and person.get("job") == "Director"
        for person in credits.get("crew", [])
    )

    if uma_is_cast and tarantino_directed:
        matches.append({
            "id": movie_id,
            "title": details.get("title"),
            "release_date": details.get("release_date"),
            "runtime": details.get("runtime"),
            "vote_average": details.get("vote_average"),
            "vote_count": details.get("vote_count"),
        })

    # Brief pause between candidate requests.
    time.sleep(0.15)

columns = [
    "id",
    "title",
    "release_date",
    "runtime",
    "vote_average",
    "vote_count",
]

df = pd.DataFrame(matches, columns=columns)

if not df.empty:
    df = df.sort_values(
        by=["runtime", "title"],
        ascending=[True, True],
        na_position="last",
    )

print("=" * 70)
print("UMA THURMAN MOVIES DIRECTED BY QUENTIN TARANTINO")
print("Sorted by runtime: shortest to longest")
print("=" * 70)

if df.empty:
    print("No matching movies were found.")
else:
    print(df.to_string(index=False))

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "uma_thurman_tarantino_search.csv"
)

df.to_csv(output_file, index=False)

print(f"\nMatching movies: {len(df)}")
print(f"Results saved to: {output_file}")
