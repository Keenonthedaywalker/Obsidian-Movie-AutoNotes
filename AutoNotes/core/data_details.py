# coding: utf8

import matplotlib
from pathlib import Path
import base64
import io
import numpy as np
from matplotlib.figure import Figure
import datetime
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast
import plotly.graph_objects as go
import plotly.io as pio

class NewDataDetails:
	def __init__(self):
		pass

	@staticmethod
	def new_count_occurences(occuringItem):
		"""
		count_occurances counts the amount of times an given item(i.e. director name or writer name or specific genre of movie) occurs in the user's movie library.

		This function uses only one parameter and that is 'occuringItem' which is the name of the item that the user want's to count. If the user wants to see the amount of times
		a director reoccurs in their library then they have to type director and it's the same principle for anything else.
		"""
		print("Hello this is my new test, you FOOL!")
		var1 = "test me."
		occuringItem = var1
		return occuringItem

	@staticmethod
	def scatter_plot_plotly():
		rng = np.random.default_rng(1234)

		# Generate data
		x = rng.lognormal(size=200)
		y = x + rng.normal(
			scale=5 * (x / np.max(x)), size=200
		)

		# Create interactive scatter plot
		fig = go.Figure(
			data=go.Scatter(
				x=x,
				y=y,
				mode="markers",
				marker=dict(
					size=10,
					opacity=0.7,
					line=dict(width=1, color="black")
				),
				customdata=np.arange(len(x)),
				hovertemplate=(
					"Point: %{customdata}<br>"
					"X: %{x:.3f}<br>"
					"Y: %{y:.3f}"
					"<extra></extra>"
				)
			)
		)

		fig.update_layout(
			width=900,
			height=600,
			template="plotly_white"
		)

		# Return HTML rather than a PNG image
		return pio.to_html(
			fig,
			full_html=False,
			include_plotlyjs="cdn"
		)

	@staticmethod
	def scatter_plot():
		rng = np.random.default_rng(1234)

		# Generate data
		x = rng.lognormal(size=200)
		y = x + rng.normal(scale=5 * (x / np.max(x)), size=200)

		# Initialize layout (Figure instead of plt.subplots, so no GUI is involved)
		fig = Figure(figsize=(9, 6))
		ax = fig.subplots()

		# Add scatterplot
		ax.scatter(x, y, s=60, alpha=0.7, edgecolors="k")

		# Save to memory and encode as text so it can go inside HTML
		buffer = io.BytesIO()
		fig.savefig(buffer, format="png", bbox_inches="tight")
		return base64.b64encode(buffer.getvalue()).decode("ascii")

	@staticmethod
	def bar_plot():
		# Data set
		height = [3, 12, 5, 18, 45]
		bars = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi']
		y_pos = np.arange(len(bars))
		
		# Initialize layout (Figure instead of plt.subplots, so no GUI is involved)
		fig = Figure(figsize=(9, 6))
		ax = fig.subplots()

		# Basic bar plot
		ax.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
		ax.set_title('Total num of genres')
		ax.set_xlabel('Most watched movie genres')
		ax.set_ylabel('Num of Genres')
		ax.set_xticks(y_pos)
		ax.set_xticklabels(bars)
		ax.tick_params(axis='x', colors='red', direction='out', length=13, width=3)
		
		# Custom Axis title
		#ax.clabel('title of the xlabel', fontweight='bold', color = 'orange', fontsize='17', horizontalalignment='center')

		# Save to memory and encode as text so it can go inside HTML
		buffer = io.BytesIO()
		fig.savefig(buffer, format="png", bbox_inches="tight")
		return base64.b64encode(buffer.getvalue()).decode("ascii")

	@staticmethod
	def time_chart():
		# Create dataframe
		dataframe = pd.DataFrame({
			'date_when_watched': [
				datetime.datetime(2021, 11, i + 1)
				for i in range(7)
			],
			'movies_watched': [5, 6, 8, 2, 3, 7, 4]
		})

		# Create figure and axes
		fig = Figure(figsize=(9, 6))
		ax = fig.subplots()

		# Plot the time series
		ax.plot(
			dataframe['date_when_watched'],
			dataframe['movies_watched'],
			marker='o'
		)

		# Configure chart
		ax.set_title('Amount of Movies Watched in Given Week')
		ax.set_xlabel('Week')
		ax.set_ylabel('Movies Watched')
		ax.tick_params(axis='x', labelrotation=30)

		fig.tight_layout()

		# Save to memory and encode as text so it can go inside HTML
		buffer = io.BytesIO()
		fig.savefig(buffer, format="png", bbox_inches="tight")
		return base64.b64encode(buffer.getvalue()).decode("ascii")


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
		# ValueError - Raised if the string isn�t a valid literal, e.g. Horror(not in quotes)
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

