
import os

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

URL = "https://api.themoviedb.org/3/discover/movie"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "accept": "application/json",
}

params = {
    "with_cast": 62,              # Bruce Willis
    "with_genres": "28,878",      # Action AND Science Fiction
    "sort_by": "vote_average.desc",
    "vote_count.gte": 100,        # Avoid movies with very few votes
    "include_adult": "false",
    "language": "en-US",
    "page": 1,
}

response = requests.get(
    URL,
    headers=headers,
    params=params,
    timeout=30,
)
response.raise_for_status()

results = response.json().get("results", [])

if not results:
    print("No matching movies found with these filters.")
else:
    df = pd.DataFrame(results)

    columns = [
        "id",
        "title",
        "release_date",
        "vote_average",
        "vote_count",
        "popularity",
    ]

    # Keep only available columns
    columns = [column for column in columns if column in df.columns]
    df = df[columns]

    df = df.sort_values(
        by=["vote_average", "vote_count"],
        ascending=[False, False],
    )

    print("=" * 65)
    print("BEST-RATED SCIENCE FICTION ACTION MOVIES")
    print("Starring Bruce Willis")
    print("=" * 65)
    print(df.to_string(index=False))

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "bruce_willis_search.csv"
    )
    df.to_csv(output_file, index=False)

    print(f"\nResults saved to: {output_file}")
    print(f"Movies found on this page: {len(df)}")
