
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

# A non-empty collection name identifies a franchise movie.
df["movie_type"] = (
    df["belongs_to_collection"]
    .fillna("")
    .str.strip()
    .ne("")
    .map({True: "Franchise", False: "Standalone"})
)

# Calculate ROI only when budget and revenue are valid.
valid_roi = (
    df["budget_musd"].gt(0)
    & df["revenue_musd"].notna()
)

df["roi_percent"] = float("nan")
df.loc[valid_roi, "roi_percent"] = (
    (
        df.loc[valid_roi, "revenue_musd"]
        - df.loc[valid_roi, "budget_musd"]
    )
    / df.loc[valid_roi, "budget_musd"]
    * 100
)

metrics = [
    "revenue_musd",
    "roi_percent",
    "budget_musd",
    "popularity",
    "vote_average",
]

summary = df.groupby("movie_type")[metrics].agg(
    ["count", "mean", "median"]
)

print("=" * 70)
print("FRANCHISE VS STANDALONE MOVIES")
print("=" * 70)

print("\nNumber of movies in each group:")
print(df["movie_type"].value_counts().to_string())

print("\nComparison of performance metrics:")
print(summary.round(2).to_string())

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "franchise_vs_standalone.csv"
)

summary.to_csv(output_file)

print(f"\nComparison saved to: {output_file}")
print("\nAnalysis completed.")
