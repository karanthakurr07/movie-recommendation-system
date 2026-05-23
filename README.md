# 🎬 CineMatch — AI Movie Recommendation System
### Built with: Python · Flask · SQLite · HTML/CSS/JavaScript

---

## What This Project Does

CineMatch is a full-stack web application that recommends movies based on your preferences.

**Concepts used (from your spec):**
- ✅ Content-based filtering (genre, era, runtime matching)
- ✅ Multi-attribute scoring (match % calculated from 4 factors)
- ✅ Relational database queries (SQLite with structured SQL)
- ✅ Forward Filtering Engine (Flask backend evaluates constraints)

---

## Project Structure

```
movie_recommender/
│
├── app.py            ← Flask backend (Inference Engine)
├── setup_db.py       ← Run once to create the database
├── movies.db         ← SQLite database (created after setup)
├── README.md         ← This file
│
└── templates/
    └── index.html    ← Frontend dashboard (HTML + CSS + JS)
```

---

## How to Run (Step by Step)

### Step 1 — Install Python
Download Python from https://python.org (version 3.8+)

### Step 2 — Install Flask
Open your terminal / command prompt and run:
```
pip install flask
```

### Step 3 — Set Up the Database
In the `movie_recommender` folder, run:
```
python setup_db.py
```
You should see: `✅ Database created with 43 movies!`

### Step 4 — Start the Web Server
```
python app.py
```
You should see: `🎬 Movie Recommender running at http://127.0.0.1:5000`

### Step 5 — Open in Browser
Go to: **http://127.0.0.1:5000**

---

## How the System Works (Beginner Explanation)

### 1. Knowledge Base (movies.db)
The SQLite database stores movies in a table with columns:
- `id`, `title`, `genres`, `release_year`, `runtime_minutes`, `rating`, `plot_summary`

### 2. Filter Engine (app.py → /recommend route)
When you click "Find My Movies", the browser sends your preferences to Flask.
Flask builds a SQL query like:
```sql
SELECT * FROM movies
WHERE (genres LIKE '%Sci-Fi%' OR genres LIKE '%Thriller%')
  AND release_year BETWEEN 1990 AND 2010
  AND runtime_minutes <= 150
ORDER BY rating DESC
```

### 3. Scoring Engine (compute_match_score function)
Each filtered movie gets a score out of 100:
- **Genre overlap** → up to 50 points
- **Viewer rating** → up to 30 points  
- **Year proximity** → up to 10 points
- **Runtime headroom** → up to 10 points

### 4. Frontend (templates/index.html)
JavaScript sends your filter selections to Flask using `fetch()`,
receives the ranked JSON results, and builds the movie cards dynamically.

---

## Example Query

**User selects:**
- Genre: Sci-Fi, Thriller
- Year range: 1990–2010
- Max runtime: 150 min

**System returns:**
1. The Matrix (1999) — 136 min — 98% Match
2. Minority Report (2002) — 145 min — 94% Match
3. Memento (2000) — 113 min — 91% Match

---

## How to Extend This Project

| Feature | How |
|---|---|
| Add more movies | Edit `setup_db.py` and re-run it |
| Add movie posters | Store image URLs in the DB, display with `<img>` |
| Add a search bar | Add a `?q=` query param and SQL `LIKE '%query%'` |
| User accounts | Use Flask-Login + add a `users` table |
| Real movie data | Use the TMDB API (free) to import thousands of movies |

---

## Technologies Used

| Layer | Technology | Purpose |
|---|---|---|
| Database | SQLite | Store the movie catalogue |
| Backend | Python + Flask | Handle requests, run SQL queries, score movies |
| Frontend | HTML + CSS + JS | User interface, sliders, cards |
| Communication | JSON (via fetch) | Browser ↔ Flask data exchange |

---

*Built as a first-year CS college project. Happy coding! 🚀*
