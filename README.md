# TMDB Movie Data Analysis

## Project Overview

This project uses Python, Pandas, and the TMDB API to collect, clean, analyze, and visualize movie data.

The analysis explores movie budgets, box-office revenue, estimated profit, return on investment (ROI), audience ratings, popularity, genres, directors, and franchise performance.

The project demonstrates a complete data analysis workflow, from API data collection and data cleaning to exploratory data analysis (EDA), visualization, and reporting.

## Project Objectives

- Collect movie data using the TMDB API.
- Clean and validate raw movie data using Pandas.
- Perform exploratory data analysis.
- Calculate key performance indicators (KPIs).
- Search for movies based on actors, directors, and genres.
- Compare franchise and standalone movie performance.
- Analyze director and franchise performance.
- Create visualizations to communicate findings.
- Document the results and limitations of the analysis.

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- Matplotlib
- Jupyter Notebook
- python-dotenv
- Git and GitHub
- PyCharm

## Data Source

Movie data is collected from [The Movie Database (TMDB)](https://www.themoviedb.org/) through its API.

The dataset includes movie titles, release dates, genres, budgets, revenue, audience ratings, popularity, cast members, directors, and other movie information.

The cleaned dataset contains 18 movies and 22 columns.

**Note:** This is a small, selected sample of movies and does not represent the entire film industry.

## Project Structure

```text
tmdb-movie-analysis/
│
├── data/
│   ├── raw/
│   │   ├── tmdb_movies_raw.json
│   │   └── fetch_failures.json
│   │
│   └── processed/
│       ├── tmdb_movies_clean.csv
│       ├── bruce_willis_search.csv
│       ├── uma_thurman_tarantino_search.csv
│       ├── franchise_vs_standalone.csv
│       ├── franchise_performance.csv
│       └── director_performance.csv
│
├── notebooks/
│   └── tmdb_movie_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── fetch_movies.py
│   ├── clean_movies.py
│   ├── validate_clean_data.py
│   ├── explore_movies.py
│   ├── analyze_kpis.py
│   ├── search_bruce_willis.py
│   ├── search_uma_thurman.py
│   ├── compare_franchises.py
│   ├── analyze_franchises.py
│   └── analyze_directors.py
│
├── reports/
│   └── figures/
│       ├── budget_vs_revenue.png
│       ├── roi_by_genre.png
│       ├── popularity_vs_rating.png
│       ├── yearly_box_office.png
│       └── franchise_vs_standalone.png
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the Repository

If the project is available on GitHub, clone it using:

```bash
git clone <https://github.com/Kamandathe3rd/tmdb-movie-analysis>
cd tmdb-movie-analysis
```

Alternatively, open the existing project folder in PyCharm.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the TMDB API Token

Create a `.env` file in the project root and added my TMDB API bearer token:

```text
TMDB_BEARER_TOKEN=
```



**Security:** Never upload your `.env` file or expose your API token publicly. Ensure `.env` is included in `.gitignore`.

## Running the Project

Run the following commands from the project root.

### 1. Fetch Movie Data

```bash
python src/fetch_movies.py
```

This script retrieves movie details and credits from the TMDB API and saves the raw responses in `data/raw/`.

### 2. Clean the Data

```bash
python src/clean_movies.py
```

This script processes the raw API responses and creates the cleaned dataset:

`data/processed/tmdb_movies_clean.csv`

### 3. Validate the Data

```bash
python src/validate_clean_data.py
```

This script checks the cleaned dataset's structure, columns, missing values, and duplicate movie IDs.

### 4. Run the Analysis Scripts

```bash
python src/explore_movies.py
python src/analyze_kpis.py
python src/search_bruce_willis.py
python src/search_uma_thurman.py
python src/compare_franchises.py
python src/analyze_franchises.py
python src/analyze_directors.py
```

These scripts perform exploratory analysis, KPI calculations, advanced movie searches, franchise comparisons, and director analysis.

### 5. Run the Jupyter Notebook

Open the following file in PyCharm or Jupyter Notebook:

`notebooks/tmdb_movie_analysis.ipynb`

Run the notebook cells from top to bottom to reproduce the analysis and visualizations.

## Analysis Performed

### 1. Data Collection and Cleaning

- Retrieved movie details and credits through the TMDB API.
- Stored raw API responses in JSON format.
- Cleaned and transformed the collected data using Pandas.
- Converted financial values into millions of US dollars.
- Checked the cleaned dataset for missing values and duplicate movie IDs.

### 2. Exploratory Data Analysis

Explored:

- Movie release dates and years.
- Production budgets and box-office revenue.
- Audience ratings and vote counts.
- TMDB popularity.
- Movie runtime.
- Genre distribution.

### 3. Key Performance Indicators

Calculated and analyzed:

- Production budgets.
- Box-office revenue.
- Estimated profit.
- Return on investment (ROI).
- Audience ratings.
- Vote counts.
- Popularity scores.

Estimated profit is calculated as:

**Profit = Revenue − Budget**

ROI is calculated as:

**ROI (%) = ((Revenue − Budget) / Budget) × 100**

These calculations exclude marketing, distribution, taxes, and other costs.

### 4. Advanced Movie Searches

**Bruce Willis Movie Search**

Identifies movies starring Bruce Willis that match the selected Action and Science Fiction genre criteria and ranks the results by audience rating.

**Uma Thurman and Quentin Tarantino Movie Search**

Identifies movies featuring Uma Thurman and directed by Quentin Tarantino, then sorts the results by runtime.

### 5. Franchise Analysis

Compares franchise and standalone movies using average revenue and ROI.

The analysis also groups movies by collection to examine movie counts, budgets, revenue, and average audience ratings.

### 6. Director Performance Analysis

Compares directors based on:

- Number of movies in the sample.
- Total box-office revenue.
- Average revenue per movie.
- Average audience rating.

## Visualizations

The Jupyter Notebook contains five visualization sections:

1. **Movie Budget vs. Revenue:** Examines the relationship between production budgets and box-office revenue.
2. **Average ROI by Genre:** Compares estimated ROI across genres.
3. **Movie Popularity vs. Audience Rating:** Explores the relationship between TMDB popularity and audience ratings.
4. **Yearly Box-Office Performance:** Compares revenue across release years represented in the sample.
5. **Franchise vs. Standalone Movies:** Compares average revenue and ROI between the two groups.

The charts are saved in `reports/figures/` for use in the final report.

## Key Findings

The analysis of the selected movies produced the following findings:

- Avengers: Endgame had the highest box-office revenue in the cleaned dataset.
- Avatar had the highest estimated profit among the sampled movies.
- James Cameron had the highest combined revenue among the directors represented in the dataset.
- Anthony Russo and Joe Russo had the highest average director ratings in the sample.
- The franchise-versus-standalone comparison revealed differences in average revenue and ROI, but the standalone group contained only two movies.

These findings apply only to the selected sample and should not be interpreted as industry-wide conclusions.

## Limitations

- The dataset contains only 18 selected movies.
- The sample is heavily weighted toward commercially successful movies.
- Different genres, directors, franchises, and years have different numbers of sampled movies.
- Only two movies are classified as standalone, limiting the reliability of that comparison.
- TMDB popularity and audience ratings can change over time.
- ROI is an estimate based on production budget and box-office revenue, not a complete measure of profitability.
- The analysis depends on the accuracy and availability of data returned by the TMDB API.

## Reproducibility

To reproduce the project:

1. Install the required Python dependencies.
2. Configure the TMDB API token in `.env`.
3. Run the data collection script.
4. Run the cleaning and validation scripts.
5. Execute the analysis scripts.
6. Run the cells in `notebooks/tmdb_movie_analysis.ipynb`.

Existing processed CSV files can be used for analysis without repeatedly fetching data from the API, provided those files are available.

## Acknowledgements

Movie data is provided by The Movie Database (TMDB).

This product uses the TMDB API but is not endorsed or certified by TMDB.