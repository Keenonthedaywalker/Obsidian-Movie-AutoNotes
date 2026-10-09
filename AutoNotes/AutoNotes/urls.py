"""
URL configuration for AutoNotes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("stats/", views.stats, name="stats"),
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("movie/<str:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movie/<str:movie_id>/add/", views.add_movie, name="add_movie"),
    path("library/<int:pk>/", views.movie_edit, name="movie_edit"),
    path("library/<int:pk>/delete/", views.movie_delete, name="movie_delete"),
    path("library/<int:pk>/export/", views.movie_export, name="movie_export"),
]