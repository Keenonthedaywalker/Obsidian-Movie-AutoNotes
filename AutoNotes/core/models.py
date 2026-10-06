from django.conf import settings
from django.db import models

class UserMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movies")
    imdb_id = models.CharField(max_length=20)

    # Details fetched from the code (saved as a snapshot)
    title = models.CharField(max_length=255)
    cover_url = models.URLField(max_length=500, blank=True)
    plot = models.TextField(blank=True)
    release_date = models.CharField(max_length=50, blank=True)
    genres = models.JSONField(default=list, blank=True)
    directors = models.JSONField(default=list, blank=True)
    writers = models.JSONField(default=list, blank=True)
    stars = models.JSONField(default=list, blank=True)

    # The user's own fields
    rating = models.PositiveSmallIntegerField(null=True, blank=True)   # 1-5
    watched_date = models.DateField(null=True, blank=True)
    opinion = models.TextField(blank=True)
    favourite_quotes = models.TextField(blank=True)

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "imdb_id")   # no duplicates per user
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"