import sqlite3
import json
from pathlib import Path

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    imdb_id TEXT PRIMARY KEY,
    title TEXT,
    year TEXT,
    imdb_rating REAL,
    json_data TEXT
)
""")

json_folder = Path("D:\\Python IMDB Scraper\\Obsidian-Movie-AutoNotes\\JSONDatabase\\movie_cache")

for json_file in json_folder.glob("*.json"):

    imdb_id = json_file.stem.split("-")[0]

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cursor.execute("""
    INSERT OR REPLACE INTO movies
    (imdb_id, title, year, imdb_rating, json_data)
    VALUES (?, ?, ?, ?, ?)
    """, (
        imdb_id,
        data.get("Title"),
        data.get("Year"),
        data.get("imdbRating"),
        json.dumps(data)
    ))

conn.commit()

cursor.execute("SELECT title FROM movies")
myresult = cursor.fetchall()

for movie_details in myresult:
    print(movie_details)

conn.close()