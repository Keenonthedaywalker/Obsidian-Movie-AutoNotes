from imdbinfo import search_title, get_movie, get_name, get_season_episodes, get_reviews, get_trivia, get_all_interests, get_filmography, TitleType, get_akas

movie_id = ""
if movie_id:
    movie = get_movie(movie_id)
    print("Movie:", movie)

# Search for a title
results = search_title("The Matrix")
for movie in results.titles:
    print(f"{movie.title} ({movie.year}) - Rating: {movie.rating} - {movie.imdb_id}")

# Get movie details
print("\n\n\n")
movie = get_movie("0133093")  # or 'tt0133093'
print(movie.title, movie.year, movie.rating)

"""# Get movie kind:
print(movie.kind)  # movie, tvSeries, tvMiniSeries, tvMovie, tvEpisode, tvSpecial, tvShort, short, videoGame, video, musicVideo, podcastEpisode, podcastSeries
print(movie.is_series())  # False

# Get person details
person = get_name("nm0000206")  # or '0000206' 
print(person.name, person.birth_date)

akas = get_akas("tt0133093")  # The Matrix
for aka in akas["akas"][:5]:
    print(f"{aka.title} ({aka.country_name})")

trivia = get_trivia("tt0133093")  # The Matrix
for fact in trivia[:3]:
    print(f"Interest Score: {fact['interestScore']}")
    print(f"Fact: {fact['body'][:200]}...")
    print("---")

movies = ["tt1490017", "tt0133093"]

for imdb_id in movies:
    interests = get_all_interests(imdb_id)
    print(f"Interests for {imdb_id}: {interests}")

filmography = get_filmography("nm0000206")  # Brad Pitt
if filmography:
    for role, films in filmography.items():
        print(f"\nRole: {role}")
        for film in films:
            print(f" - {film.title} ({film.year}) [{film.imdbId}]")

# Search for single type: movies
results = search_title("The Matrix", title_type=TitleType.Movies)
for movie in results.titles:
    print(f"{movie.title} ({movie.year}) - {movie.imdb_id}")
"""
html_write = open("index.html", "w")

html_write.write(f'<html>\n<head>\n<title> \nOutput Data in an HTML file \
           </title>\n</head> <body><h1>Welcome to <u>GeeksforGeeks</u></h1>\
           \n<h2>A <u>CS</u> Portal for Everyone</h2> \n<img src="{movie.cover_url}"></body></html>')

html_write.close()