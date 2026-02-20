## Obsidian Movie AutoNotes

### Description
Obsidian Movie AutoNotes is a Python-based application that automates the process of collecting, organizing, and analyzing movie data.

The program allows users to provide a list of movie titles, retrieves detailed metadata for each film, and generates structured Markdown notes designed for integration with Obsidian. 
In addition to note creation, the system stores all collected data in a structured CSV format, enabling further analysis and visualization.

(Personal Note)
I started working on this project because, I was spending a lot of my free time copying and pasting details from movies for my own personal Obsidian vault, and eventually realised that there was a much simpler way to get the information I needed, and also a much simpler way to generate notes.
Thanks, Python!

### Requirements
If you intend to use this program, then you need to have [Obsidian](https://obsidian.md/) installed, with the [Colored Text](https://github.com/erincayaz/obsidian-colored-text) plugin that can be found in the Community Plugins tab in Obsidian.

You also need to have python installed and you need to install all of the libraries that are listed in the requirements.txt file as well.

### Usage
To Use this program, open the movies.txt file, input the movies you want to create notes for into the text file, and then run the main.py file. 

It might take a while to run depending on how many movies you put in the file.

You will know it's done once you see the histogram appears with all of occurences of directors on it(See note below if you want to remove this).

If you want to retrieve certain details from a movie and not others, you can use the specific functions in the class.

*Text file with list of movies*

<img width="654" height="528" alt="UsageExample1" src="https://github.com/user-attachments/assets/51ffd39b-4a79-4210-851b-88e2871cb77e" />


*Terminal with results after running program*
<img width="984" height="489" alt="UsageExample3" src="https://github.com/user-attachments/assets/0c2d49c8-c735-40a7-9572-261505e6d582" />


*Histogram with top 10 most occuring directors*
<img width="1006" height="667" alt="UsageExample2" src="https://github.com/user-attachments/assets/f7e28a60-83b9-485c-919e-164b33a2e8a0" />


*Histogram with top 25 most occuring actors*
<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/417577ce-761c-4182-aed2-fc96b9f6106a" />


*Movie Base file with all movie cards that were created with the program*
<img width="1910" height="1034" alt="Screenshot 2026-02-20 214241" src="https://github.com/user-attachments/assets/d7d96a4d-89b7-41d7-a378-803fba5a68e6" />


*Note of Movie with all of the generated information*
<img width="1572" height="1039" alt="Screenshot 2026-02-20 214334" src="https://github.com/user-attachments/assets/a6df14ba-392b-45b7-a28d-8daba6bab733" />


#### Other Usage Examples: 

```python
occurences = data_handler.count_occurrences("directors", split_values=True)
print(occurences)
```
Result: > {'Terry Jones': 2, 'Christopher Nolan': 2, 'James Cameron': 2, 'Mali Finn': 2}

```python
the_matrix = MovieInfo("0109151")
print(the_matrix.get_movie_taglines())
```
Result: > ["If humans don't want me... why'd they create me?"]

```python
# * means that it will print all list items on their own, seperately
print(*the_matrix.get_cast_with_roles(), sep=", ")
```
Result: > Elizabeth Berkley, Kiefer Sutherland, Dan Woren, Wanda Nowicki, Mike Reynolds, Bryan Cranston

(Note: Don't input duplicates of the movie or run the same movies twice, if you have an interest in the data aspect of this program, because, as of right now, doing this will result in duplicate results being made in the csv file. 
This has no impact on the creation of the Obsidian notes however, so if you only care about the notes, feel free to remove the functions involving the DataDetails class.)
**Delete below code if not interested in the Data**
'''python
data_handler = DataDetails("movies_data.csv")
data_handler.save_movies(all_movies)

occurences = data_handler.count_occurrences("directors", split_values=True)
print(occurences)

data_handler.histogram("directors", 10, split_values=True)
'''

## TODO
 - Add function to check if series or movie
 - Add genre search function
 - Improve look of graphs
 - Add more graphs
 - Add class or function or both for the creating the movies so that it isn't just in a for loop
 - Fix issue that creates duplicate details of films in csv file when running same movie more than once
 - CSV File sort alphabetically

## Team

Just me, Keenon!
