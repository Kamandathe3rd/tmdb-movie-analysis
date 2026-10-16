
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"

df = pd.read_csv(CSV_FILE)

# Convert release dates into proper datetime values
df["release_date"] = pd.to_datetime(
    df["release_date"], errors="coerce"
)

# Extract the release year
df["release_year"] = df["release_date"].dt.year

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# 1. Dataset overview
print("\n1. DATASET OVERVIEW")
print(f"Number of movies: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print(f"Date range: {df['release_date'].min()} to {df['release_date'].max()}")

# 2. Summary statistics
print("\n2. NUMERICAL SUMMARY")
numeric_columns = [
    "budget_musd",
    "revenue_musd",
    "vote_average",
    "vote_count",
    "popularity",
    "runtime",
]
print(df[numeric_columns].describe().round(2))

# 3. Missing and empty values
print("\n3. MISSING AND EMPTY VALUES")
empty_counts = (
    df.astype("str")
    .apply(lambda column: column.str.strip().eq("").sum())
)
missing_counts = df.isna().sum()

missing_summary = pd.DataFrame({
    "missing_values": missing_counts,
    "empty_strings": empty_counts,
})

print(missing_summary.to_string())

# 4. Movies released by year
print("\n4. MOVIES BY RELEASE YEAR")
print(
    df["release_year"]
    .value_counts()
    .sort_index()
    .to_string()
)

# 5. Most common genres
print("\n5. MOST COMMON GENRES")
genre_counts = (
    df.assign(genres=df["genres"].fillna("").str.split("|"))
    .explode("genres")
)

genre_counts["genres"] = genre_counts["genres"].str.strip()
genre_counts = genre_counts[
    genre_counts["genres"].ne("")
]

print(genre_counts["genres"].value_counts().head(10).to_string())

# 6. Highest-rated movies
print("\n6. TOP 5 MOVIES BY RATING")
print(
    df.nlargest(5, "vote_average")[
        ["title", "vote_average", "vote_count"]
    ].to_string(index=False)
)

# 7. Most popular movies
print("\n7. TOP 5 MOVIES BY POPULARITY")
print(
    df.nlargest(5, "popularity")[
        ["title", "popularity", "vote_average"]
    ].to_string(index=False)
)

# 8. Highest-revenue movies
print("\n8. TOP 5 MOVIES BY REVENUE (USD MILLIONS)")
print(
    df.nlargest(5, "revenue_musd")[
        ["title", "budget_musd", "revenue_musd"]
    ].to_string(index=False)
)

print("\nEDA completed successfully.")
