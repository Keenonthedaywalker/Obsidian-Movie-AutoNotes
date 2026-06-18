from imdbinfo import (
    get_trivia,
    get_movie as imdb_get_movie,
    search_title,
    TitleType
)
from obsidian_notes import ObsidianNote
from data_details import DataDetails
from collections.abc import Iterable
from pathlib import Path
import json
import requests
import re
import html

CACHE_DIR = Path("D:\\Python IMDB Scraper\\Obsidian-Movie-AutoNotes\\JSONDatabase\\movie_cache")
CACHE_DIR.mkdir(exist_ok=True)


API_KEY = "2622ff3"

class MovieInfo:

	def __init__(self):
		self.movie = None		   # OMDb JSON
		self.imdb_movie = None     # imdbinfo object
		self.movie_trivia = []
		self.imdb_id = None
			

	# This fixes any potential names that might have otherwise caused issues with the formatting.
	# For instance the markdown file for Alien: Covenant wasn't being created, because windows doesn't allow filenames with the colon in. 
	def safe_filename(self, name):
		return re.sub(r'[\\/*?:"<>|]', '', name)

	# Search for movies that are given to the function via the file parameter.
	# Return the id's of said movies.
	def file_movie_search(self, file):

		movie_id_list = []

		with open(file, 'r') as f:

			for line in f:
				line = line.strip()

				if not line:
					continue

				search_results = search_title(line, title_type=TitleType.Movies)

				print(search_results.titles[0])
				
				if search_results:
					movie_id = search_results.titles[0].imdb_id
					print("Movie:", line, "| IMDb ID:", movie_id)
					movie_id_list.append(movie_id)
		
		return movie_id_list
	

	def get_movie(self, movie_id):

		movie_id = str(movie_id)

		if movie_id.startswith("tt"):
			tt_id = movie_id
		else:
			tt_id = f"tt{movie_id}"

		self.imdb_id = tt_id

		# Look for an existing cache file
		existing_files = list(CACHE_DIR.glob(f"{movie_id}-*.json"))

		if existing_files:

			cache_file = existing_files[0]

			print("Loaded from cache:", cache_file)

			with open(cache_file, "r", encoding="utf-8") as f:
				self.movie = json.load(f)

		else:

			print("Fetching from API:", tt_id)

			response = requests.get(
				"https://www.omdbapi.com/",
				params={
					"apikey": API_KEY,
					"i": tt_id,
					"plot": "full"
				}
			)

			self.movie = response.json()

			movie_title = self.safe_filename(
				self.movie.get("Title", "Unknown")
			)

			cache_file = CACHE_DIR / f"{movie_id}-{movie_title}.json"

			print("Saving to:", cache_file)

			with open(cache_file, "w", encoding="utf-8") as f:
				json.dump(self.movie, f, indent=4)

			print("Saved successfully!")

		return self.movie


	def get_movie_title(self):
		title = self.movie["Title"]
		print(title)
		return title

	def get_movie_cover_url(self):
		movie_cover = self.movie["Poster"]
		print(movie_cover)
		return movie_cover

	def get_movie_plot(self):
		plot = self.movie["Plot"]
		print(plot)
		return plot

	def get_movie_genres(self):

		genres = self.movie.get("Genre", "N/A")

		if genres == "N/A":
			return []

		genre_list = [g.strip() for g in genres.split(",")]

		print(genre_list)

		return genre_list


	def get_movie_directors(self):

		# I use get here because sometimes directors is represented with N/A so using get here will help for checking it on the next line.
		directors = self.movie.get("Director")

		if not directors or directors == "N/A":
			return []

		the_directors = [d.strip() for d in directors.split(",")]

		for director in the_directors:
			print(f" - {director}")

		return the_directors

	def get_movie_writers(self):

		writers = self.movie.get("Writer", "N/A")

		if writers == "N/A":
			return []

		the_writers = [w.strip() for w in writers.split(",")]

		for writer in the_writers:
			print(f" - {writer}")

		return the_writers

	def get_cast_with_roles(self):

		actors = self.movie.get("Actors", "N/A")

		if actors == "N/A":
			return []

		cast = []

		for actor in actors.split(",")[:8]:
			actor = actor.strip()
			print(f" - {actor}")
			cast.append(actor)

		return cast

	def get_movie_release_date(self):
		release_date = self.movie["Year"]
		print(release_date)
		return release_date

	def get_movie_trivia(self):

		if self.imdb_id is None:
			print("No IMDb ID")
			return []

		try:
			trivia = get_trivia(self.imdb_id)

			print(f"Loaded {len(trivia)} trivia items")

			return trivia

		except Exception as e:
			print(f"Trivia failed: {e}")
			return []

	# This function checks for the which method was used to provide movie ids, then returns those ids in list form
	def all_movie_details(self, source):
		# Checks if it's a file path
		if isinstance(source, str) and Path(source).is_file():
			with open(source, "r", encoding="utf-8") as f:
				movie_ids = [line.strip() for line in f if line.strip()]

		# Checks if it's a single string ID
		elif isinstance(source, str):
			movie_ids = [source]

		# Checks if it's a list/tuple
		elif isinstance(source, Iterable):
			movie_ids = list(source)

		# Otherwise calls this error message
		else:
			raise ValueError("Invalid input type.")

		# Load movies
		return [mid for mid in movie_ids]



	def create_note_for_movie(self):
		note = ObsidianNote(
			# The Path to your Obsidian Vault where you want to create notes
			# Example: vault_path=r"D:\\Obsidian Vaults\\Movies"
			vault_path=r"",
			# Note name
			movie_name=self.safe_filename(f"{movie_title} ({movie_release_date})")
		)

		note.set_properties(
			moviePoster=movie_cover,
			directors=movie_directors,
			writers=movie_writers,
			stars=movie_stars,
			dateReleased=movie_release_date,
			dateWatched=None,
			myScore=None,
			personalThoughts="Testing",
			favQuote="Wow, what a great quote!",
			favScene=None,
			trivia=None
		)

		# The Body content of the notes
		note.set_body(f"""
## {movie_title} ({movie_release_date})

### <span style="color:rgb(146, 208, 80)">Movie Poster: </span>
![movie_cover]({movie_cover})

## Summary
{movie_plot}

### <span style="color:rgb(112, 48, 160)">Genres</span>
{movie_genres_body} {movie_genres_tags}

### <span style="color:rgb(6, 152, 72)">Directors:</span>
{movie_directors_body} {movie_director_tags}

### <span style="color:rgb(0, 176, 240)">Writers:</span>
{movie_writers_body} {movie_writer_tags}

### <span style="color:rgb(255, 192, 0)">Stars: </span>
{movie_stars_body} \n{movie_stars_tags}

### <span style="color:rgb(200, 91, 251)">Date Released: </span>
{movie_release_date}

### <span style="color:rgb(2, 242, 182)">Date Watched:</span>
Fill In Your Own Info Here

### <span style="color:rgb(154, 86, 29)">My Score:</span>
Fill In Your Own Info Here

### <span style="color:rgb(112, 48, 160)">Personal Thoughts:</span>
Fill In Your Own Info Here

### <span style="color:rgb(0, 112, 192)">Favourite Quote:</span>
Fill In Your Own Info Here

### <span style="color:rgb(146, 208, 80)">Favourite Scene: </span>
Fill In Your Own Info Here

### <span style="color:rgb(43, 166, 51)">Trivia</span>
{movie_trivia_body}

""")

		note.save()

# This function is used to create tags
def names_to_tags(names):
	cleaned_tags = []

	for name in names:
		# Remove anything that is not a letter or number
		clean_name = re.sub(r'[^a-zA-Z0-9]', '', name)
		cleaned_tags.append(f"#{clean_name}")

	return " ".join(html.unescape(cleaned_tags))

# This function is used to retrieve movie details and converts them into a structured dictionary with properly formatted list fields for analysis in the form of a csv file
def movie_to_dict(the_movie, movie_id):

	genres_str = " | ".join(the_movie.get_movie_genres())
	directors_str = " | ".join(the_movie.get_movie_directors())
	writers_str = " | ".join(the_movie.get_movie_writers())
	stars_str = " | ".join(the_movie.get_cast_with_roles())

	genres_list = re.split(r'\s*\|\s*', genres_str)
	directors_list = re.split(r'\s*\|\s*', directors_str)
	writers_list = re.split(r'\s*\|\s*', writers_str)
	stars_list = re.split(r'\s*\|\s*', stars_str)

	return {
		"movie_id": movie_id,
		"title": the_movie.get_movie_title(),
		"year": the_movie.get_movie_release_date(),
		"genres": genres_list,
		"directors": html.unescape(directors_list),
		"stars": html.unescape(stars_list),
		"writers": writers_list
	}

all_movies = []

#pythonmovie = ia.get_movie('0133093')  # The Matrix
#print(movie.keys())  # See all available keys

# Class Initializer
my_movie = MovieInfo()

movie_id_list = my_movie.file_movie_search("D:\\Python IMDB Scraper\\Obsidian-Movie-AutoNotes\\movies.txt")


# Loop through list of movie ids, find the details of all the id's provided
for movie_id in movie_id_list:
	# This would look like this, MovieInfo("0109151")
	the_movie = MovieInfo()
	movie = the_movie.get_movie(movie_id)
	movie_title = the_movie.get_movie_title()

	# Skip failed movies
	if the_movie.movie is None:
		continue

	movie_cover = the_movie.get_movie_cover_url()
	movie_title = the_movie.get_movie_title()
	movie_plot = the_movie.get_movie_plot()

	movie_genres = the_movie.get_movie_genres()
	movie_genres_body = ", ".join(movie_genres)
	movie_genres_tags = names_to_tags(movie_genres)

	movie_directors = the_movie.get_movie_directors()
	movie_directors_body = ", ".join(movie_directors)
	movie_director_tags = names_to_tags(movie_directors)

	movie_writers = the_movie.get_movie_writers()
	movie_writers_body = ", ".join(movie_writers)
	movie_writer_tags = names_to_tags(movie_writers)

	movie_stars = the_movie.get_cast_with_roles()
	movie_stars_body = "\n".join(f"- {html.unescape(s)}" for s in movie_stars)

	# Pass only the names (before the " - ") to names_to_tags
	star_names = [html.unescape(s.split(" - ")[0]) for s in movie_stars]
	movie_stars_tags = names_to_tags(star_names)

	movie_release_date = the_movie.get_movie_release_date()

	movie_trivia = the_movie.get_movie_trivia()
	movie_trivia_body = "\n".join(f"- {html.unescape(d['body'])}" for d in movie_trivia[:5])

	the_movie.create_note_for_movie()

	movie_dict = movie_to_dict(the_movie, movie_id)

	all_movies.append(movie_dict)

print(all_movies)

data_handler = DataDetails("movies_data.csv")
#data_handler.save_movies(all_movies)

#occurences = data_handler.count_occurrences("directors", split_values=True)
#print(occurences)

# Display the 10 most frequent occurances in the data
#data_handler.histogram("directors", 10, split_values=True)
