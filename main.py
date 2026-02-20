from imdb import Cinemagoer
from obsidian_notes import ObsidianNote
from data_details import DataDetails
from collections.abc import Iterable
from pathlib import Path
import re

class MovieInfo:

	def __init__(self, movie_id=None):
		self.ia = Cinemagoer()
		self.movie = None
		self.all_movies = []

		if movie_id:
			self.movie = self.ia.get_movie(movie_id)

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

				search_results = self.ia.search_movie(line)
				
				if search_results:
					movie_id = search_results[0].movieID
					print("Movie:", line, "| IMDb ID:", movie_id)
					movie_id_list.append(movie_id)
		
		return movie_id_list



	# This function is useful for when you want information on a certain movie, but forgot the specific name of said movie.
	# It returns the names, ids and dates of all movies and series that are relevant to the input the user gave.
	def movie_search(self):
		movie_search = input("Movie: ")
		return self.ia.search_movie(movie_search)

	# Returns a list of the top rated movies.
	# Takes one parameter that is either 
	def display_top_250_movies(self):
		top_movies = ia.get_top250_movies()

		for i, movie in enumerate(top_movies):
			print(i, "-", movie['title'], "| IMDb ID:", movie.movieID)

		return top_movies

	# Get the infosets about the movie
	def get_movie_infoset(self):
		return self.movie.infoset2keys

	def get_movie_title(self):
		title = self.movie.get('title')
		return title

	def get_movie_cover_url(self):
		movie_cover = self.movie.get('cover url')
		return movie_cover

	def get_movie_plot(self):
		plot = self.movie.get('plot')
		return plot[0]

	def get_movie_genres(self):
		genres = self.movie.get('genres', [])
		return genres


	def get_movie_directors(self):
		directors = self.movie.get('directors', [])
		return [person['name'] for person in directors]

	def get_movie_writers(self):
		writers = self.movie.get('writers', [])
		return [person['name'] for person in writers]

	# For the time being, roles are broken in the cinemagoer library, and aren't being displayed for whatever reason, however cast members are being displayed.
	def get_cast_with_roles(self):
		cast = self.movie.get('cast', [])[:6]
		return [person['name'] for person in cast]

	def get_movie_release_date(self):
		return self.movie.get('year')

	def get_movie_trivia(self):
		self.ia.update(self.movie, info=['trivia'])
		trivia = self.movie.get('trivia', [])
		return trivia

	def get_movie_taglines(self):
		self.ia.update(self.movie, info=['taglines'])
		taglines = self.movie.get('taglines', [])
		return taglines

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
			taglines=movie_taglines,
			genres=movie_genres,
			directors=movie_directors,
			writers=movie_writers,
			stars=movie_stars,
			dateReleased=movie_release_date,
			dateWatched=None,
			myScore=None,
			personalThoughts="Testing",
			favQuote="Wow, what a great quote!",
			favScene=None,
			trivia=movie_trivia
		)

		# The Body content of the notes
		note.set_body(f"""
## {movie_title} ({movie_release_date})

### <span style="color:rgb(146, 208, 80)">Movie Poster: </span>
![movie_cover]({movie_cover})

## Taglines
{movie_taglines_body}

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


### <span style="color:rgb(154, 86, 29)">My Score:</span>


### <span style="color:rgb(112, 48, 160)">Personal Thoughts:</span>


### <span style="color:rgb(0, 112, 192)">Favourite Quote:</span>


### <span style="color:rgb(146, 208, 80)">Favourite Scene: </span>


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

	return " ".join(cleaned_tags)

# This function is used to retrieve movie details and converts them into a structured dictionary with properly formatted list fields for analysis in the form of a csv file
def movie_to_dict(movie_id):
	the_movie = MovieInfo(movie_id)

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
		"directors": directors_list,
		"writers": writers_list,
		"stars": stars_list
	}

all_movies = []

# Class Initializer
my_movie = MovieInfo()

# Here we provide the function with a .txt file with the names of various movies in it. 
# It then proceeds to search for the information of all of the movies that are listed.
movie_id_list = my_movie.file_movie_search("movies.txt")

# Search through the provided list for movies of the same name
# Return movie ids
movie_list = my_movie.all_movie_details(movie_id_list)
print(movie_list)


# Loop through list of movie ids, find the details of all the id's provided
for movie_id in movie_list:
	# This would look like this, MovieInfo("0109151")
	the_movie = MovieInfo(movie_id)

	movie_cover = the_movie.get_movie_cover_url()
	movie_title = the_movie.get_movie_title()
	movie_plot = the_movie.get_movie_plot()

	movie_taglines = the_movie.get_movie_taglines()
	movie_taglines_body = "\n".join(f"- {d}" for d in movie_taglines)

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
	movie_stars_body = "\n".join(f"- {d}" for d in movie_stars)
	movie_stars_tags = names_to_tags(movie_stars)

	movie_release_date = the_movie.get_movie_release_date()

	movie_trivia = the_movie.get_movie_trivia()
	movie_trivia_body = "\n".join(f"- {d}" for d in movie_trivia)
	movie_trivia_tags = names_to_tags(movie_trivia)


	movie_to_dict(movie_id)

	the_movie.create_note_for_movie()

	movie_dict = movie_to_dict(movie_id)

	all_movies.append(movie_dict)

print(all_movies)

data_handler = DataDetails("movies_data.csv")
data_handler.save_movies(all_movies)

occurences = data_handler.count_occurrences("directors", split_values=True)
print(occurences)

# Display the 10 most frequent occurances in the data
data_handler.histogram("directors", 10, split_values=True)
