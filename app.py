"""
app.py  —  Flask Backend (Inference / Forward Filtering Engine)
Run with: python app.py
Visit:     http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import math

app = Flask(__name__)
DB_PATH = "movies.db"


#  Database helper
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # access columns by name
    return conn


#  Scoring Engine
def compute_match_score(movie, selected_genres, year_min, year_max, max_runtime):
    """
    Multi-attribute scoring:
      - Genre overlap   → up to 50 points
      - Rating bonus    → up to 30 points
      - Year proximity  → up to 10 points
      - Runtime bonus   → up to 10 points
    Returns a 0–100 integer score.
    """
    movie_genres = [g.strip() for g in movie["genres"].split(",")]

    # 1. Genre overlap score
    matched = sum(1 for g in selected_genres if g in movie_genres)
    genre_score = (matched / max(len(selected_genres), 1)) * 50

    # 2. Rating bonus  (scale 0–10 → 0–30)
    rating_score = (movie["rating"] / 10) * 30

    # 3. Year proximity (closer to midpoint of range = better)
    mid_year = (year_min + year_max) / 2
    year_range = max(year_max - year_min, 1)
    year_diff = abs(movie["release_year"] - mid_year)
    year_score = max(0, 10 - (year_diff / year_range) * 10)

    # 4. Runtime bonus (more headroom = slightly better)
    runtime_headroom = max_runtime - movie["runtime_minutes"]
    runtime_score = min(10, runtime_headroom / 10)

    total = genre_score + rating_score + year_score + runtime_score
    return min(99, max(1, math.floor(total)))


#  Main recommendation route
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    # Parse user preferences
    selected_genres = data.get("genres", [])           # list of strings
    year_min        = int(data.get("year_min", 1970))
    year_max        = int(data.get("year_max", 2024))
    max_runtime     = int(data.get("max_runtime", 240))

    #  Step 1: Build SQL query (structural column filtering)
    # Genre filter: movie must contain AT LEAST ONE selected genre
    # Using LIKE for substring match on comma-separated genres column
    conn = get_db()
    cursor = conn.cursor()

    if selected_genres:
        genre_conditions = " OR ".join(["genres LIKE ?" for _ in selected_genres])
        genre_params     = [f"%{g}%" for g in selected_genres]
        sql = f"""
            SELECT * FROM movies
            WHERE ({genre_conditions})
              AND release_year BETWEEN ? AND ?
              AND runtime_minutes <= ?
            ORDER BY rating DESC
        """
        params = genre_params + [year_min, year_max, max_runtime]
    else:
        sql = """
            SELECT * FROM movies
            WHERE release_year BETWEEN ? AND ?
              AND runtime_minutes <= ?
            ORDER BY rating DESC
        """
        params = [year_min, year_max, max_runtime]

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({"movies": [], "message": "No movies matched your filters. Try widening the criteria!"})

    # Step 2: Score & rank each result
    scored = []
    for row in rows:
        movie = dict(row)
        movie["match_score"] = compute_match_score(
            movie, selected_genres, year_min, year_max, max_runtime
        )
        # Build genre tags list
        movie["genre_list"] = [g.strip() for g in movie["genres"].split(",")]
        # Explain WHY it was selected
        matched_genres = [g for g in selected_genres if g in movie["genre_list"]]
        movie["why_selected"] = _explain(movie, matched_genres, year_min, year_max, max_runtime)
        scored.append(movie)

    # Sort by match score descending, take top 8
    scored.sort(key=lambda m: m["match_score"], reverse=True)
    top = scored[:8]

    return jsonify({"movies": top, "total_found": len(rows)})


def _explain(movie, matched_genres, year_min, year_max, max_runtime):
    """Generate a human-readable explanation of why this movie was recommended."""
    reasons = []
    if matched_genres:
        reasons.append(f"Matches genre{'s' if len(matched_genres)>1 else ''}: {', '.join(matched_genres)}")
    if year_min <= movie["release_year"] <= year_max:
        reasons.append(f"Released in {movie['release_year']} (within your era {year_min}–{year_max})")
    if movie["runtime_minutes"] <= max_runtime:
        reasons.append(f"Runtime {movie['runtime_minutes']} min ≤ your limit of {max_runtime} min")
    reasons.append(f"Viewer rating: {movie['rating']}/10")
    return " · ".join(reasons)


# Home page 
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    print("🎬 Movie Recommender running at http://127.0.0.1:5000")
    app.run(debug=True)
