
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

# Keep only movies with a collection name.
franchises = df[
    df["belongs_to_collection"].notna()
    & df["belongs_to_collection"].str.strip().ne("")
].copy()

# Group movies by collection and calculate performance metrics.
summary = (
    franchises.groupby("belongs_to_collection")
    .agg(
        movie_count=("id", "count"),
        total_budget_musd=("budget_musd", "sum"),
        mean_budget_musd=("budget_musd", "mean"),
        total_revenue_musd=("revenue_musd", "sum"),
        mean_revenue_musd=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean"),
    )
    .sort_values("total_revenue_musd", ascending=False)
)

print("=" * 75)
print("FRANCHISE PERFORMANCE ANALYSIS")
print("=" * 75)

print("\nFranchise summary (sorted by total revenue):")
print(summary.round(2).to_string())

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "franchise_performance.csv"
)

summary.to_csv(output_file)

print(f"\nResults saved to: {output_file}")
print("\nFranchise analysis completed.")
