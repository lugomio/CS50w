from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="title"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
