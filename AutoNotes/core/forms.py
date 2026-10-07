from django import forms
from .models import UserMovie

class UserMovieForm(forms.ModelForm):
    class Meta:
        model = UserMovie
        fields = ["rating", "watched_date", "opinion", "favourite_quotes", "favourite_scene_url"]
        widgets = {
            "watched_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "opinion": forms.Textarea(attrs={"rows": 5, "placeholder": "What did you think?"}),
            "favourite_quotes": forms.Textarea(attrs={"rows": 4, "placeholder": "One quote per line..."}),
            "favourite_scene_url": forms.URLInput(attrs={"placeholder": "https://example.com/scene.jpg"}),
        }