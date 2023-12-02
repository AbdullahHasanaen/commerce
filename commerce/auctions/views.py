from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listing,Comment,Bid

def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListings,
        "categories":allCategories,
    })

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html",{
        "id":id,
        "listing":listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments":allComments,
        "isOwner": isOwner
    })
def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']


    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message

    )

    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def closeAuction(request,id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "id": id,
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update":True,
        "message": "Congratulations! Your auction is closed"
    })

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
def displayWatchlis(request):
    currentUser = request.user
    listing = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listing":listing
    })

def removeWatchlist (request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
def addWatchlist (request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories,
    })
def addBid(request,id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message": "Bid was updated successfully"
            "update",
            "isListingInWatchlist":isListingInWatchlist,
            "allComments":allComments,
            "isOwner": isOwner,

        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid was updated Failed"
                       "update",
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,

        })

def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request,"auctions/create.html",{
            'categories': allCategories
        })
    else:
        #Get the data from the fotm
        request.method == "POST"
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        #Who is the user?
        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)

        bid = Bid(bid=int(price), user=currentUser)
        bid.save()
        # create a new listing
        newListing = Listing(
            title=title,
            description=description,
            imgUrl=imageurl,
            price=bid,
            category=categoryData,
            owner=currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
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
