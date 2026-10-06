from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from .your_main_file import some_function

@login_required
def home(request):
    # result = some_function()
    result = f"Welcome, {request.user.username}!"
    return render(request, "core/home.html", {"result": result})

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