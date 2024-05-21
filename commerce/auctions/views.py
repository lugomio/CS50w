from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, WatchList, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active=True).all()
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

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids_count = Bid.objects.filter(listing=listing).all().count
    watchlist_item = None
    in_watchlist = False
    comments = Comment.objects.filter(listing = listing).all()

    if request.user.is_authenticated:
        watchlist_item = WatchList.objects.filter(user=request.user, listing=listing).first()
        in_watchlist = watchlist_item and watchlist_item.listing == listing

    if request.method == "POST":
        bidder = request.user
        price = request.POST.get("price", None)

        if not bidder or not listing or not price or float(price) <= listing.price or listing.active == False:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids_count": bids_count,
                "message": "An error occurred while creating your biding, please try again.",
                "in_watchlist": in_watchlist,
                "comments": comments
            })
        
        try:
            bid = Bid.objects.create(
                bidder = bidder,
                listing = listing,
                price = price
            )
            bid.save()

            listing.price = float(price)
            listing.winner = bidder
            listing.save()

        except IntegrityError:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids_count": bids_count,
                "message": "An error occurred while creating your biding, please try again.",
                "in_watchlist": in_watchlist,
                "comments": comments
            })
        
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bids_count": bids_count,
            "in_watchlist": in_watchlist,
            "comments": comments
        })

def category_item(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category = category, active = True).all()

    return render(request, "auctions/category_item.html", {
        "listings": listings,
        "category": category
    })

def category(request):
    categorys = Category.objects.all()

    return render(request, "auctions/categorys.html", {
        "categorys": categorys
    })


def watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    action = request.POST.get("action", None)

    if not listing or not action:
        return HttpResponseRedirect(reverse('watchlist_list'))

    if request.method == "POST":
        if action == "add":
            try:
                watchlist = WatchList.objects.create(
                    user = request.user,
                    listing = listing
                )
                watchlist.save()
            except IntegrityError:
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        elif action == "remove":
            try:
                watchlist = WatchList.objects.get(listing = listing, user = request.user)
                watchlist.delete()
            except IntegrityError:
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        else:
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
def watchlist_list(request):
    return render(request, "auctions/watchlist.html", {
        "watchlists": WatchList.objects.filter(user = request.user)
    })

def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    try:
        listing.active = False
        listing.save()
    except IntegrityError:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

def comment(request, listing_id):

    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        autor = request.user
        comment_text = request.POST.get("comment", None)
        
        if not listing or not autor or not comment_text:
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        
        try:
            comment = Comment.objects.create(
                autor = autor,
                comment = comment_text,
                listing = listing
            )
            comment.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))