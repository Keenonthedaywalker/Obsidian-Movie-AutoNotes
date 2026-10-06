from pathlib import Path
import yaml


class ObsidianNote:
	def __init__(self, vault_path, movie_name):
		self.vault_path = Path(vault_path)
		self.movie_name = movie_name
		self.note_path = self.vault_path / f"{movie_name}.md"
		self.properties = {}
		self.body = ""

	# Set movie properties (YAML frontmatter)
	def set_properties(
		self,
		moviePoster="",
		taglines="",
		genres="",
		directors=None,
		writers=None,
		stars=None,
		dateReleased="",
		dateWatched=None,
		myScore=None,
		personalThoughts="",
		favQuote="",
		favScene="",
		trivia=""
	):
		
		# Avoid mutable default arguments because otherwise you might get same results
		directors = directors or []
		writers = writers or []
		stars = stars or []

		self.properties = {
			"moviePoster": moviePoster,
			"taglines": taglines,
			"genres": genres,
			"directors": directors,
			"writers": writers,
			"stars": stars,
			"dateReleased": dateReleased,
			"dateWatched": dateWatched,
			"myScore": myScore,
			"personalThoughts": personalThoughts,
			"favQuote": favQuote,
			"favScene": favScene,
			"trivia": trivia,
		}

	# Set the markdown body of the note
	def set_body(self, markdown_text):
		self.body = markdown_text

	# Build the full note text
	def build_note(self):
		yaml_block = yaml.dump(self.properties, sort_keys=False, allow_unicode=True)
		return f"---\n{yaml_block}---\n{self.body}"

	# Save the note to the vault
	def save(self):
		full_note = self.build_note()
		self.note_path.write_text(full_note, encoding="utf-8")
		print(f"Created note: {self.note_path}")



