from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
import datetime


def index(request):
    listings = Listing.objects.filter(active=True).order_by('-id')
    return render(request, "auctions/index.html", {"listings": listings, "heading": "Active Listings"})

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
    unusable_names = ['admin', 'categories', 'watchlist']
    for cat in Category.objects.all():
        unusable_names.append(cat.category)
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
            if username.upper() not in (name.upper() for name in unusable_names):
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                Watchlist.objects.create(user=user)
            else:
                return render(request, "auctions/register.html", {
                "message": "Username cannot be taken."
            })
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })  
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data["description"]
            title = form.cleaned_data["listing_title"]
            starting_price = form.cleaned_data["starting_price"]
            user = request.user
            image = form.cleaned_data["image"]
            category = Category.objects.get(id=int(request.POST["category"]))
        listing=Listing.objects.create(title=title, description=description, starting_price=starting_price, seller=user, image=image)
        listing.save
        category.listings.add(listing)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "form": NewListingForm(),
        "categories": Category.objects.all(),
        "red": None,
        })

@login_required
def watchlist(request):
    user= request.user
    watchlist = Watchlist.objects.get(user=user)
    listings = watchlist.listings.all()
    return render(request, "auctions/index.html", {"watchlist":watchlist, "listings":listings, "heading":f"{request.user.username}\'s Watchlist"})

def listing(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if request.user.is_authenticated:
            item = Listing.objects.get(pk=listing_id)
            bid = request.POST.get("bid")
            if bid != None:
                if int(bid) > item.current_price:
                    b = Bid.objects.create(buyer=request.user, listing=item, bid=int(bid))
                    item.current_price = int(bid)
                    item.save()
                    b.save()
                else:
                    return render(request, "auctions/listing.html", {"listing":item, "message": "Bid should be more than current price"})
            status = request.POST.get("watchlist")
            if status != None:
                watchlist = Watchlist.objects.get(user=request.user)
                listings = watchlist.listings.all()
                if item in listings:
                    request.user.watchlist.listings.remove(item)
                else:
                    request.user.watchlist.listings.add(item)
            closed = request.POST.get("close")
            if closed != None:
                item.active = False
                item.save()
                return render(request, "auctions/listing.html", {"listing":item,"closed":True, "comments": item.comments.all(), "buyer": item.bids.get(bid=item.current_price).buyer})
            comment=request.POST.get("comment")
            if comment != None:
                new_comment = Comment.objects.create(user=request.user, listing=item, comment=comment, time=datetime.datetime.now())
            return HttpResponseRedirect(reverse('listing', args=(item.id,)))
    if request.user.is_authenticated:
        user = request.user
        if item.active == False:
            return render(request, "auctions/listing.html", {"listing":item,"closed":True, "comments": item.comments.all(), "buyer": item.bids.get(bid=item.current_price).buyer})
        return render(request, "auctions/listing.html", {"listing":item,"Watchlist":Watchlist.objects.get(user=user), "comments": item.comments.all(), "form":NewCommentForm()})
    
    return render(request, "auctions/listing.html", {"listing":item, "comments": item.comments.all()})


def categories(request):
    return render(request, "auctions/categories.html", {"categories": Category.objects.all()})

def category(request, category):
    c = Category.objects.get(category=category)
    listings = c.listings.filter(active=True)
    return render(request, "auctions/index.html", {"heading":f"Active Listings under {c.category}", "listings":listings})

def person_listings(request, username):
    user = User.objects.get(username=username)
    listings = user.listings.all()
    return render(request, "auctions/index.html", {"heading":f"{user.username}\'s Listings", "listings":listings})