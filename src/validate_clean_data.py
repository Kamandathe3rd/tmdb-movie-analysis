
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

print("=" * 50)
print("CLEANED DATASET VALIDATION")
print("=" * 50)

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes.to_string())

print("\nDuplicate movie IDs:")
print(df["id"].duplicated().sum())

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nMovie titles:")
print(df[["id", "title"]].to_string(index=False))

print("\nFinancial summary (USD millions):")
print(df[["budget_musd", "revenue_musd"]].describe().round(2))

expected_columns = [
    "id", "title", "tagline", "release_date", "genres",
    "belongs_to_collection", "original_language", "budget_musd",
    "revenue_musd", "production_companies", "production_countries",
    "vote_count", "vote_average", "popularity", "runtime",
    "overview", "spoken_languages", "poster_path", "cast",
    "cast_size", "director", "crew_size",
]

print("\nColumn order correct:", df.columns.tolist() == expected_columns)
print("Validation finished.")
