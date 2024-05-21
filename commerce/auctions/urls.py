from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("category/<int:category_id>", views.category_item, name="category_item"),
    path("watchlist/", views.watchlist_list, name="watchlist_list"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
