
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

# Split multiple director names into separate rows.
directors = df[
    df["director"].notna()
    & df["director"].str.strip().ne("")
].copy()

directors["director"] = directors["director"].str.split("|")
directors = directors.explode("director")

directors["director"] = directors["director"].str.strip()
directors = directors[directors["director"].ne("")]

# Calculate director performance metrics.
summary = (
    directors.groupby("director")
    .agg(
        movie_count=("id", "nunique"),
        total_revenue_musd=("revenue_musd", "sum"),
        mean_revenue_musd=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean"),
    )
    .sort_values("total_revenue_musd", ascending=False)
)

print("=" * 75)
print("DIRECTOR PERFORMANCE ANALYSIS")
print("=" * 75)

print("\nDirectors sorted by total revenue:")
print(summary.round(2).to_string())

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "director_performance.csv"
)

summary.to_csv(output_file)

print(f"\nResults saved to: {output_file}")
print("\nDirector analysis completed.")
