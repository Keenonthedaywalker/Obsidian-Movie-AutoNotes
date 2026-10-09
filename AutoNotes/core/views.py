from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import Http404
from .main import search_movies_query, get_movie_details, get_single_movie_details
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import UserMovie
from .forms import UserMovieForm
from django.http import HttpResponse
from django.utils.text import slugify
import json
from collections import Counter
from django.db.models import Avg
# from .your_main_file import some_function

@login_required
def home(request):
    return render(request, "core/home.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()        # saves to SQLite with a hashed password
            login(request, user)      # log them in right away
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def stats(request):
    return render(request, "core/stats.html")

@login_required
def profile(request):
    movies = UserMovie.objects.filter(user=request.user)
    stats = {
        "total": movies.count(),
        "average_rating": movies.aggregate(avg=Avg("rating"))["avg"],
        "directors": count_field(movies, "directors"),
        "genres": count_field(movies, "genres"),
        "stars": count_field(movies, "stars", clean=lambda s: s.split(" - ")[0]),
    }
    return render(request, "core/profile.html", {"movies": movies, "stats": stats})

@login_required
def search(request):
    query = request.GET.get("q", "").strip()
    results = search_movies_query(query) if query else []
    return render(request, "core/search.html", {"query": query, "results": results})


@login_required
def movie_detail(request, movie_id):
    movie = get_single_movie_details(movie_id)
    if movie is None:
        raise Http404("Movie not found")
    in_list = UserMovie.objects.filter(user=request.user, imdb_id=movie_id).first()
    return render(request, "core/movie_detail.html", {"movie": movie, "in_list": in_list})

@login_required
@require_POST
def add_movie(request, movie_id):
    details = get_single_movie_details(movie_id)
    if details is None:
        raise Http404("Movie not found")

    entry, created = UserMovie.objects.get_or_create(
        user=request.user,
        imdb_id=movie_id,
        defaults={
            "title": details["title"],
            "cover_url": details["cover"] or "",
            "plot": details["plot"] or "",
            "taglines": details["taglines"] or [],      # <- new
            "release_date": str(details["release_date"] or ""),
            "genres": details["genres"],
            "directors": details["directors"],
            "writers": details["writers"],
            "stars": details["stars"],
        },
    )
    return redirect("movie_edit", pk=entry.pk)

@login_required
def movie_edit(request, pk):
    # Filtering by user means nobody can open another user's entry
    entry = get_object_or_404(UserMovie, pk=pk, user=request.user)
    if request.method == "POST":
        form = UserMovieForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("movie_edit", pk=entry.pk)
    else:
        form = UserMovieForm(instance=entry)
    # The order is 10 down to 1 because the CSS reverses the row, which makes the stars appear as 1 to 10 left to right and fills leftwards on hover.
    return render(request, "core/movie_edit.html", {
    "movie": entry, "form": form, "stars": range(10, 0, -1),
    })

@login_required
@require_POST
def movie_delete(request, pk):
    entry = get_object_or_404(UserMovie, pk=pk, user=request.user)
    entry.delete()
    return redirect("profile")

def _yaml(value):
    # A JSON string is also a valid YAML double-quoted string, so quotes,
    # colons and line breaks in the user's text can't break the frontmatter.
    return json.dumps(value or "", ensure_ascii=False)

@login_required
def movie_export(request, pk):
    m = get_object_or_404(UserMovie, pk=pk, user=request.user)

    quotes = [q.strip() for q in m.favourite_quotes.splitlines() if q.strip()]
    rating = m.rating or 0
    score = f"{'★' * rating}{'☆' * (10 - rating)} | {rating}/10"
    watched = m.watched_date.isoformat() if m.watched_date else ""

    lines = [
        "---",
        f"moviePoster: {_yaml(m.cover_url)}",
        f"movieTaglines: {_yaml(' | '.join(m.taglines))}",
        f"directors: {_yaml(', '.join(m.directors))}",
        f"writers: {_yaml(', '.join(m.writers))}",
        "stars:",
        *[f"  - {_yaml(s)}" for s in m.stars],
        f"dateReleased: {_yaml(m.release_date)}",
        f"dateWatched: {watched}",
        f"myScore: {_yaml(score)}",
        f"personalThoughts: {_yaml(m.opinion)}",
        f"favQuote: {_yaml(' / '.join(quotes))}",
        f"favScene: {_yaml(m.favourite_scene_url)}",
        "---",
        "",
        '### <span style="color:rgb(146, 208, 80)">Movie Poster: </span>',
        f"![]({m.cover_url})" if m.cover_url else "",
        "",
        '### <span style="color:rgb(211, 197, 126)">Taglines:</span>',
        *[f"- {t}" for t in m.taglines],
        "",
        '### <span style="color:rgb(6, 152, 72)">Directors:</span>',
        ", ".join(m.directors),
        "",
        '### <span style="color:rgb(0, 176, 240)">Writers:</span>',
        ", ".join(m.writers),
        "",
        '### <span style="color:rgb(255, 192, 0)">Stars: </span>',
        *[f"  - {s}" for s in m.stars],
        "",
        '### <span style="color:rgb(200, 91, 251)">Date Released: </span>',
        m.release_date,
        "",
        '### <span style="color:rgb(2, 242, 182)">Date Watched:</span>',
        watched,
        "",
        '### <span style="color:rgb(154, 86, 29)">My Score:</span>',
        score,
        "",
        '### <span style="color:rgb(112, 48, 160)">Personal Thoughts:</span>',
        m.opinion,
        "",
        '### <span style="color:rgb(0, 112, 192)">Favourite Quote:</span>',
        *[f'*"{q}"*' for q in quotes],
        "",
        '### <span style="color:rgb(146, 208, 80)">Favourite Scene: </span>',
        f"![]({m.favourite_scene_url})" if m.favourite_scene_url else "",
        "",
    ]

    response = HttpResponse("\n".join(lines), content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{slugify(m.title) or "movie"}.md"'
    return response


def count_field(movies, field, top=10, min_count=1, clean=None):
    counter = Counter()
    for m in movies:
        values = getattr(m, field) or []
        if clean:
            values = [clean(v) for v in values]
        counter.update(set(values))   # set(): a name repeated within one movie counts once
    return [(name, n) for name, n in counter.most_common(top) if n >= min_count]