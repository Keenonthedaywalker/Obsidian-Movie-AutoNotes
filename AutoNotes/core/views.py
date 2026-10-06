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
def profile(request):
    movies = UserMovie.objects.filter(user=request.user)
    return render(request, "core/profile.html", {"movies": movies})

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
    return render(request, "core/movie_edit.html", {
        "movie": entry, "form": form, "stars": [5, 4, 3, 2, 1],
    })

@login_required
@require_POST
def movie_delete(request, pk):
    entry = get_object_or_404(UserMovie, pk=pk, user=request.user)
    entry.delete()
    return redirect("profile")

@login_required
def movie_export(request, pk):
    m = get_object_or_404(UserMovie, pk=pk, user=request.user)

    quotes = [q.strip() for q in m.favourite_quotes.splitlines() if q.strip()]
    tags = [slugify(g) for g in m.genres]
    title = m.title.replace('"', '\\"')

    lines = [
        "---",
        f'title: "{title}"',
        f"released: {m.release_date}",
        f"rating: {m.rating or ''}",
        f"watched: {m.watched_date or ''}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
    ]
    if m.cover_url:
        lines += [f"![poster]({m.cover_url})", ""]
    lines += [
        f"# {m.title}",
        "",
        f"**Genres:** {', '.join(m.genres)}",
        f"**Directors:** {', '.join(m.directors)}",
        f"**Writers:** {', '.join(m.writers)}",
        "",
        "## Plot",
        m.plot,
        "",
        "## Cast",
        *[f"- {s}" for s in m.stars],
        "",
        "## My Opinion",
        m.opinion or "_No opinion yet._",
        "",
        "## Favourite Quotes",
        *([f"> {q}" for q in quotes] or ["_None yet._"]),
    ]

    response = HttpResponse("\n".join(lines), content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{slugify(m.title) or "movie"}.md"'
    return response