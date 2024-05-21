from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "active_listenings": Listing.objects.filter(active=True).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        if not title or not description or not price:
            return render(request, "auctions/create.html", {
                "message": "Please, complete the required fields.",
                "categorys": Category.objects.all()
            })

        banner = request.POST.get("banner", None)
        created_by = request.user

        category_id = request.POST.get("category", None)
        if category_id:
            try:
                category = Category.objects.get(pk=int(category_id))
            except Category.DoesNotExist:
                category = None
        else:
            category = None

        try:
            listing = Listing.objects.create(
                title=title,
                description=description,
                price=price,
                banner=banner,
                category=category,
                created_by=created_by
            )
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "An error occurred while creating your listing, please try again.",
                "categorys": Category.objects.all()
            })
        return HttpResponseRedirect(reverse("create"))
    else:
        return render(request, "auctions/create.html", {
            "categorys": Category.objects.all()
        })
