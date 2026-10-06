from imdbinfo import search_title, get_movie, get_trivia, get_filmography, TitleType
from .obsidian_notes import ObsidianNote
from .data_details import DataDetails
from collections.abc import Iterable
from pathlib import Path
import random
import time
import re

class MovieInfo:

	def __init__(self):
		self.movie = None
		self.movie_trivia = []

	def load(self, movie_id):
		time.sleep(random.uniform(3, 8))

		try:
			self.movie = get_movie(movie_id)

		except Exception as e:
			print(f"Failed to load {movie_id}: {e}")
			self.movie = None
			

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



	# This function is useful for when you want information on a certain movie, but forgot the specific name of said movie.
	# It returns the names, ids and dates of all movies and series that are relevant to the input the user gave.
	def movie_get(self):
		movie = get_movie("0133093")  # or 'tt0133093'
		print(movie.title, movie.year, movie.rating, movie.plot, movie.cover_url)

	def get_movie_title(self):
		title = self.movie.title
		print(title)
		return title

	def get_movie_cover_url(self):
		movie_cover = self.movie.cover_url
		print(movie_cover)
		return movie_cover

	def get_movie_plot(self):
		plot = self.movie.plot
		print(plot)
		return plot

	def get_movie_genres(self):
		genres = self.movie.genres
		print(genres)
		return genres


	def get_movie_directors(self):
		directors = self.movie.directors
		the_directors = []
		for director in directors:
			the_directors.append(director.name)
			print(f"  - {director.name} ({director.imdbId})")
		return the_directors

	def get_movie_writers(self):
		writers = self.movie.categories["cast"]
		the_writers = []
		for writer in writers:
			if writer.job == "writer":
				the_writers.append(writer.name)
				print(f"  - {writer.name} ({writer.imdbId})")
		return the_writers

	# For the time being, roles are broken in the cinemagoer library, and aren't being displayed for whatever reason, however cast members are being displayed.
	def get_cast_with_roles(self):
		"""cast = []
		movie_id = f"tt{self.movie.imdb_id}"
		for p in self.movie.categories["cast"][:8]:
			character = None
			filmography_results = get_filmography(p.id)
			if filmography_results:
				for role, films in filmography_results.items():
					for film in films:
						if film.imdbId == movie_id:
							character = role
							break
			if character:
				cast.append(f"{p.name}")
			else:
				cast.append(f"{p.name}")
		return cast"""
		return [p.name for p in self.movie.categories["cast"][:8]]

	def get_movie_release_date(self):
		release_date = self.movie.release_date
		print(release_date)
		return release_date

	def get_movie_trivia(self):
		trivia = self.movie_trivia
		for index, fact in enumerate(trivia[:5]):
			print("---")
			print(f"Interest Score: {fact['interestScore']}")
			print(f"Fact #{index}: {fact['body'][:200]}...")
			print("---")
		return trivia

	def get_movie_taglines(self):
		# getattr with a default works whether or not the field exists
		taglines = getattr(self.movie, 'taglines', None) or []
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



	def create_note_for_movie(self, cover, title, plot, taglines_body, genres_body, genres_tags, directors, directors_body, director_tags, writers, writers_body, writer_tags, stars, stars_body, stars_tags, release_date, trivia_body):
		note = ObsidianNote(
			# The Path to your Obsidian Vault where you want to create notes
			# Example: vault_path=r"D:\\Obsidian Vaults\\Movies"
			vault_path=r"",
			# Note name
			movie_name=self.safe_filename(f"{title} ({release_date})")
		)

		note.set_properties(
			moviePoster=cover,
			directors=directors,
			writers=writers,
			stars=stars,
			dateReleased=release_date,
			dateWatched=None,
			myScore=None,
			personalThoughts="Testing",
			favQuote="Wow, what a great quote!",
			favScene=None,
			trivia=None
		)

		"""note.set_properties(
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
			trivia=None
		)"""

		# The Body content of the notes
		note.set_body(f"""
## {title} ({release_date})

### <span style="color:rgb(146, 208, 80)">Movie Poster: </span>
![movie_cover]({cover})

## Taglines
{taglines_body}

## Summary
{plot}

### <span style="color:rgb(112, 48, 160)">Genres</span>
{genres_body} {genres_tags}

### <span style="color:rgb(6, 152, 72)">Directors:</span>
{directors_body} {director_tags}

### <span style="color:rgb(0, 176, 240)">Writers:</span>
{writers_body} {writer_tags}

### <span style="color:rgb(255, 192, 0)">Stars: </span>
{stars_body} \n{stars_tags}

### <span style="color:rgb(200, 91, 251)">Date Released: </span>
{release_date}

### <span style="color:rgb(2, 242, 182)">Date Watched:</span>


### <span style="color:rgb(154, 86, 29)">My Score:</span>


### <span style="color:rgb(112, 48, 160)">Personal Thoughts:</span>


### <span style="color:rgb(0, 112, 192)">Favourite Quote:</span>


### <span style="color:rgb(146, 208, 80)">Favourite Scene: </span>


### <span style="color:rgb(43, 166, 51)">Trivia</span>
{trivia_body}

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
def movie_to_dict(the_movie, movie_id):

	genres_str = " | ".join(the_movie.get_movie_genres())
	directors_str = " | ".join(the_movie.get_movie_directors())
	#writers_str = " | ".join(the_movie.get_movie_writers())
	stars_str = " | ".join(the_movie.get_cast_with_roles())

	genres_list = re.split(r'\s*\|\s*', genres_str)
	directors_list = re.split(r'\s*\|\s*', directors_str)
	#writers_list = re.split(r'\s*\|\s*', writers_str)
	stars_list = re.split(r'\s*\|\s*', stars_str)

	return {
		"movie_id": movie_id,
		"title": the_movie.get_movie_title(),
		"year": the_movie.get_movie_release_date(),
		"genres": genres_list,
		"directors": directors_list,
		"stars": stars_list
		#"writers": writers_list
	}

all_movies = []

#pythonmovie = ia.get_movie('0133093')  # The Matrix
#print(movie.keys())  # See all available keys

# Class Initializer
my_movie = MovieInfo()

# Here we provide the function with a .txt file with the names of various movies in it. 
# It then proceeds to search for the information of all of the movies that are listed.
movie_id_list = my_movie.file_movie_search("D:\\Obsidian Notes\\Obsidian-Movie-AutoNotes\\AutoNotes\\core\\movies.txt")

# Search through the provided list for movies of the same name
# Return movie ids
movie_list = my_movie.all_movie_details(movie_id_list)
print(movie_list)

def get_single_movie_details(movie_id, save_note=False):
    the_movie = MovieInfo()
    the_movie.load(movie_id)

    if the_movie.movie is None:
        return None

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
    movie_stars_body = "\n".join(f"- {s}" for s in movie_stars)
    star_names = [s.split(" - ")[0] for s in movie_stars]
    movie_stars_tags = names_to_tags(star_names)
	
    trivia = the_movie.get_movie_trivia()
    trivia_facts = [d["body"] for d in trivia[:5]]
    movie_trivia_body = "\n".join(f"- {d['body']}" for d in trivia[:5])

    movie_release_date = the_movie.get_movie_release_date()
	
    details = {
        "id": movie_id,
        "cover": movie_cover,
        "title": movie_title,
        "plot": movie_plot,
        "taglines": movie_taglines,
        "genres": movie_genres,
        "directors": movie_directors,
        "writers": movie_writers,
        "stars": movie_stars,
        "release_date": movie_release_date,
        "trivia": trivia_facts,
    }

    if save_note:
        the_movie.create_note_for_movie(movie_cover, movie_title, movie_plot, movie_taglines_body, movie_genres_body, movie_genres_tags, movie_directors, movie_directors_body, movie_director_tags, movie_writers, movie_writers_body, movie_writer_tags, movie_stars, movie_stars_body, movie_stars_tags, movie_release_date, movie_trivia_body)

    return details

def get_movie_details(movie_ids):
    all_movies = []
    for movie_id in movie_ids:
        details = get_single_movie_details(movie_id)
        if details:
            all_movies.append(details)
    return all_movies

def search_movies_query(query, limit=10):
    results = search_title(query)
    return [
        {"id": t.imdb_id, "title": t.title, "year": t.year}
        for t in results.titles[:limit]
    ]


if __name__ == "__main__":
    movie_list = ["0109151"]
    for mid in movie_list:
        print(get_single_movie_details(mid, save_note=True))