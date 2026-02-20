from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import ast


class DataDetails:
	def __init__(self, file_path):
		self.file_path = Path(file_path)

	def load_data(self):
		if self.file_path.exists():
			self.df = pd.read_csv(self.file_path)
		else:
			self.df = pd.DataFrame()

	def save_movies(self, movies_list):

		if not movies_list:
			print("No movies to save.")
			return

		df_new = pd.DataFrame(movies_list)

		# Force movie_id to string
		df_new["movie_id"] = df_new["movie_id"].astype(str)

		self.load_data()

		if not self.df.empty:
			self.df["movie_id"] = self.df["movie_id"].astype(str)
			self.df = pd.concat([self.df, df_new], ignore_index=True)
			self.df = self.df.drop_duplicates(subset="movie_id")
		else:
			self.df = df_new

		self.df.to_csv(self.file_path, index=False)

		print(f"Saved {len(df_new)} movies to {self.file_path}")


	def convert_to_list(self, cell_value):
		try:
			# Convert string representation of list to actual list
			# The cell_value might look like this, "['Action', 'Comedy']"
			# The below code basically evaluates Python literals and converts it into whatever it is
			# For example: literal_eval() succeeds then it returns: ['Action', 'Comedy']
			return ast.literal_eval(cell_value)
		# ValueError - Raised if the string isn’t a valid literal, e.g. Horror(not in quotes)
		# SyntaxError - Raised if the string is malformed, e.g. ['Horror', 'Comedy'(not closed properly with bracket)
		# TypeError - Raised if the value isn't a string, e.g. None
		except (ValueError, SyntaxError, TypeError):
			# If it's not a list, just return as a single-element list
			return [cell_value]

	# Count occurence of column name in the data
	def count_occurrences(self, column_name, split_values=False):

		self.load_data()

		# Split multi-value cells into lists
		df = self.df.copy()

		if split_values:
			# This runs convert_to_list() on every cell in the column
			df[column_name] = df[column_name].apply(self.convert_to_list)
			# explode takes a list in a cell and creates one row per list item
			# Example: Genres - ["Action", "Horror"], ["Comedy"]
			# Genres - Action, Horror, Comedy
			df = df.explode(column_name)

		# Counts how often each value appears
		return df[column_name].value_counts().to_dict()

	# Create histogram and chart the provided data
	def histogram(self, column_name, n, split_values=False):

		# Load dataset
		self.load_data()
		df = self.df.copy()

		if split_values:
			# This runs convert_to_list() on every cell in the column
			df[column_name] = df[column_name].apply(self.convert_to_list)
			# explode takes a list in a cell and creates one row per list item
			df = df.explode(column_name)

		# Count occurrences
		counts = df[column_name].value_counts().head(n)

		# Plot
		plt.style.use("dark_background")
		figure, ax = plt.subplots(figsize=(10, 6))

		# barh = Bar Horizontal
		counts.plot(kind="barh", ax=ax)

		ax.set_title(f"Most Common {column_name} Occurrences in Movies", fontsize=14)
		ax.set_xlabel("Frequency")

		ax.invert_yaxis()
		plt.tight_layout()
		plt.show()

