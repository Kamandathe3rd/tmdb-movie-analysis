
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "tmdb_movies_raw.json"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def join_names(items):
    """Convert a list of TMDB objects into pipe-separated names."""
    if not isinstance(items, list):
        return np.nan

    names = [
        item.get("name")
        for item in items
        if isinstance(item, dict) and item.get("name")
    ]

    return "|".join(names) if names else np.nan


def extract_collection(value):
    """Extract the collection name from a TMDB collection object."""
    if not isinstance(value, dict):
        return np.nan

    return value.get("name") or np.nan


def extract_cast(credits, limit=10):
    """Return the first ten credited cast members."""
    if not isinstance(credits, dict):
        return np.nan

    cast = credits.get("cast", [])
    if not isinstance(cast, list):
        return np.nan

    names = [
        person.get("name")
        for person in cast[:limit]
        if isinstance(person, dict) and person.get("name")
    ]

    return "|".join(names) if names else np.nan


def extract_director(credits):
    """Extract director names from the crew credits."""
    if not isinstance(credits, dict):
        return np.nan

    crew = credits.get("crew", [])
    if not isinstance(crew, list):
        return np.nan

    directors = [
        person.get("name")
        for person in crew
        if isinstance(person, dict)
        and person.get("job") == "Director"
        and person.get("name")
    ]

    return "|".join(dict.fromkeys(directors)) if directors else np.nan


def extract_crew_size(credits):
    """Count crew records returned by TMDB."""
    if not isinstance(credits, dict):
        return np.nan

    crew = credits.get("crew", [])
    return len(crew) if isinstance(crew, list) else np.nan


def main():
    # Load raw responses without modifying the original file.
    with RAW_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    rows = []

    for record in records:
        details = record.get("details", {})
        credits = record.get("credits", {})

        if not isinstance(details, dict):
            continue

        # Start with all fields returned by the movie details endpoint.
        row = details.copy()

        # Flatten nested fields into analysis-friendly values.
        row["belongs_to_collection"] = extract_collection(
            details.get("belongs_to_collection")
        )
        row["genres"] = join_names(details.get("genres"))
        row["production_companies"] = join_names(
            details.get("production_companies")
        )
        row["production_countries"] = join_names(
            details.get("production_countries")
        )
        row["spoken_languages"] = join_names(
            details.get("spoken_languages")
        )

        # Add cast and crew information.
        cast = credits.get("cast", []) if isinstance(credits, dict) else []
        row["cast"] = extract_cast(credits)
        row["cast_size"] = len(cast) if isinstance(cast, list) else np.nan
        row["director"] = extract_director(credits)
        row["crew_size"] = extract_crew_size(credits)

        rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No movie details were available to clean.")

    logging.info("Initial DataFrame shape: %s", df.shape)

    # Remove columns not needed for the analysis.
    columns_to_drop = [
        "adult",
        "imdb_id",
        "original_title",
        "video",
        "homepage",
        "backdrop_path",
        "origin_country",
        "softcore",
    ]

    df.drop(
        columns=columns_to_drop,
        errors="ignore",
        inplace=True,
    )

    # Convert numeric fields safely.
    numeric_columns = [
        "id",
        "budget",
        "revenue",
        "popularity",
        "runtime",
        "vote_count",
        "vote_average",
        "cast_size",
        "crew_size",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # Parse release dates; invalid dates become missing.
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce",
    )

    # Missing/placeholder text should not be treated as real information.
    for column in ["overview", "tagline"]:
        if column in df.columns:
            df[column] = df[column].replace(
                r"^\s*$",
                np.nan,
                regex=True,
            )

    # TMDB often uses zero for unknown financial figures or runtime.
    for column in ["budget", "revenue", "runtime"]:
        df.loc[df[column] == 0, column] = np.nan

    # Convert budget and revenue to millions of US dollars.
    df["budget_musd"] = df["budget"] / 1_000_000
    df["revenue_musd"] = df["revenue"] / 1_000_000
    df.drop(columns=["budget", "revenue"], inplace=True)

    # Remove duplicate movie IDs and records lacking essential identity.
    df.drop_duplicates(subset=["id"], keep="first", inplace=True)
    df.dropna(subset=["id", "title"], inplace=True)

    # Keep only released movies.
    if "status" in df.columns:
        df = df[df["status"] == "Released"].copy()
        df.drop(columns=["status"], inplace=True)

    # Remove records with very little information.
    minimum_values = 10
    before_filter = len(df)
    df = df[df.notna().sum(axis=1) >= minimum_values].copy()

    logging.info(
        "Rows removed by the minimum-data rule: %s",
        before_filter - len(df),
    )

    # Put the assignment's requested columns in the exact order.
    final_columns = [
        "id",
        "title",
        "tagline",
        "release_date",
        "genres",
        "belongs_to_collection",
        "original_language",
        "budget_musd",
        "revenue_musd",
        "production_companies",
        "production_countries",
        "vote_count",
        "vote_average",
        "popularity",
        "runtime",
        "overview",
        "spoken_languages",
        "poster_path",
        "cast",
        "cast_size",
        "director",
        "crew_size",
    ]

    for column in final_columns:
        if column not in df.columns:
            df[column] = np.nan

    df = df[final_columns].reset_index(drop=True)

    # Save the cleaned dataset.
    output_file = PROCESSED_DIR / "tmdb_movies_clean.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    # Print a concise validation summary.
    print("\nCLEANING SUMMARY")
    print("=" * 40)
    print(f"Raw records: {len(records)}")
    print(f"Cleaned records: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    print(f"Saved to: {output_file}")

    print("\nMissing values by column:")
    print(df.isna().sum().sort_values(ascending=False).to_string())

    print("\nCleaned data preview:")
    print(df[["id", "title", "budget_musd", "revenue_musd"]].head())

    print("\nFinal DataFrame shape:", df.shape)


if __name__ == "__main__":
    main()
