
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

# Calculate profit in USD millions.
# Profit = revenue - budget.
df["profit_musd"] = df["revenue_musd"] - df["budget_musd"]

# Calculate ROI as a percentage.
# Exclude missing or zero budgets to avoid invalid calculations.
valid_roi = (
    df["budget_musd"].notna()
    & df["budget_musd"].gt(0)
    & df["revenue_musd"].notna()
)

df["roi_percent"] = float("nan")
df.loc[valid_roi, "roi_percent"] = (
    (df.loc[valid_roi, "revenue_musd"]
     - df.loc[valid_roi, "budget_musd"])
    / df.loc[valid_roi, "budget_musd"]
    * 100
)


def show_ranking(title, data, columns, ascending=False, top_n=5):
    """Display a ranked list of movies using the selected column."""
    ranked = data.sort_values(
        by=columns[0],
        ascending=ascending,
        na_position="last",
    )

    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    print(
        ranked[columns]
        .head(top_n)
        .round(2)
        .to_string(index=False)
    )


# 1. Highest revenue
show_ranking(
    "1. HIGHEST REVENUE (USD MILLIONS)",
    df,
    ["revenue_musd", "title", "budget_musd"],
)

# 2. Highest budget
show_ranking(
    "2. HIGHEST BUDGET (USD MILLIONS)",
    df,
    ["budget_musd", "title", "revenue_musd"],
)

# 3. Highest profit
show_ranking(
    "3. HIGHEST PROFIT (USD MILLIONS)",
    df,
    ["profit_musd", "title", "revenue_musd", "budget_musd"],
)

# 4. Lowest profit
show_ranking(
    "4. LOWEST PROFIT (USD MILLIONS)",
    df,
    ["profit_musd", "title", "revenue_musd", "budget_musd"],
    ascending=True,
)

# Restrict ROI rankings to movies with budgets of at least $10 million.
eligible_roi = df[
    df["budget_musd"].ge(10)
    & df["roi_percent"].notna()
].copy()

# 5. Highest ROI
show_ranking(
    "5. HIGHEST ROI (BUDGET >= $10 MILLION)",
    eligible_roi,
    ["roi_percent", "title", "budget_musd", "revenue_musd"],
)

# 6. Lowest ROI
show_ranking(
    "6. LOWEST ROI (BUDGET >= $10 MILLION)",
    eligible_roi,
    ["roi_percent", "title", "budget_musd", "revenue_musd"],
    ascending=True,
)

# 7. Most voted
show_ranking(
    "7. MOST VOTED MOVIES",
    df,
    ["vote_count", "title", "vote_average"],
)

# 8. Highest-rated movies with at least 10 votes.
# This threshold is low because the current sample already has many votes.
rated_movies = df[df["vote_count"].ge(10)].copy()

show_ranking(
    "8. HIGHEST RATED (AT LEAST 10 VOTES)",
    rated_movies,
    ["vote_average", "title", "vote_count"],
)

# 9. Lowest-rated movies with at least 10 votes
show_ranking(
    "9. LOWEST RATED (AT LEAST 10 VOTES)",
    rated_movies,
    ["vote_average", "title", "vote_count"],
    ascending=True,
)

# 10. Most popular
show_ranking(
    "10. MOST POPULAR MOVIES",
    df,
    ["popularity", "title", "vote_average"],
)

print("\nKPI analysis completed successfully.")
