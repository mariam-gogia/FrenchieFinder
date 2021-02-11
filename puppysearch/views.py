
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm, Textarea
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Color, Listing, Location, Review


def render_with_pagination(request, listings):
    """
    Function renders the index page with pagination
    """
    paginator = Paginator(listings, per_page=10)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)
    context = {
        'listings': listings,
        'page': page,
    }
    return render(request, "puppysearch/index.html", context)


def index(request):
    """
    Index page displays active listing, newest listing first
    """
    listings = Listing.objects.all().filter(is_active=True).order_by('-timestamp')
    return render_with_pagination(request, listings)


def colors(request):
    """
    Displays all color categories of the puppies
    """
    return render(request, "puppysearch/colors.html", {"colors": Color.objects.all()})


def show_color_listings(request, color_id):
    """
    Shows active listings in the specific color category,
    newest first
    """
    if not Color.objects.all().filter(pk=color_id).exists():
        return render(request, "puppysearch/error.html", {"message": "No such color"})
    listings = Listing.objects.all().filter(color=color_id, is_active=True).order_by('-timestamp')
    return render_with_pagination(request, listings)


def show_location_listings(request, location_id):
    """
    Shows active listings in the specific location,
    newest first
    """
    if not Location.objects.all().filter(pk=location_id).exists():
        return render(request, "puppysearch/error.html", {"message": "No such location"})
    listings = Listing.objects.all().filter(location=location_id, is_active=True).order_by('-timestamp')
    return render_with_pagination(request, listings)


def show_breeder_listings(request, breeder_id):
    """
    Shows specific breeder's active listings,
    newest first
    """
    if not User.objects.all().filter(pk=breeder_id).exists():
        return render(request, "puppysearch/error.html", {"message": "No such breeder"})
    listings = Listing.objects.all().filter(breeder=breeder_id, is_active=True).order_by('-timestamp')
    return render_with_pagination(request, listings)


def show_favorites(request):
    listings = request.user.favorites.all()
    return render_with_pagination(request, listings)


def my_listings(request):
    """
    Shows user his/her listings
    """
    listings = Listing.objects.all().filter(breeder=request.user, is_active=True).order_by("-timestamp")
    return render_with_pagination(request, listings)


def my_reviews(request):
    """
    Displays given and recieved reviews of
    the logged in user
    """
    recieved_reviews = Review.objects.all().filter(reviewed=request.user).order_by("-timestamp")
    given_reviews = Review.objects.all().filter(reviewer=request.user).order_by("-timestamp")
    context = {
        "recieved_reviews": recieved_reviews,
        "given_reviews": given_reviews
    }
    return render(request, "puppysearch/my_reviews.html", context)


def breeders(request):
    """
    Shows the list of breeders
    """
    # sort alphabetically by the company name
    breeders_set = User.objects.all().filter(is_breeder=True).order_by("company_name")
    context = {
        'breeders': breeders_set,
    }
    return render(request, "puppysearch/breeders.html", context)


def locations(request):
    """
    Shows the list of locations
    """
    locations = Location.objects.all().order_by("city")
    context = {
        'locations': locations
    }
    return render(request, "puppysearch/locations.html", context)


def search(request):
    """
    Allows user to search for puupies using various fields
    """
    query = request.GET.get("q", "")
    if(Listing.objects.all().filter(id__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(id__contains=query, is_active=True))

    if(Listing.objects.all().filter(title__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(title__contains=query, is_active=True))

    if(User.objects.all().filter(company_name__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(breeder__company_name__contains=query, is_active=True))

    if(Color.objects.all().filter(name__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(color__name__contains=query, is_active=True))

    if(Location.objects.all().filter(city__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(location__city__contains=query, is_active=True))

    if(Location.objects.all().filter(state__contains=query).exists()):
        return render_with_pagination(request, Listing.objects.all().filter(location__state__contains=query, is_active=True))

    else:
        return render_with_pagination(request, "")


def profile(request, breeder_id, page_num):
    """
    Contains all the information regarding the breeder
    including his/her reviews
    """
    breeder = User.objects.get(id=breeder_id)
    num_active_listings = Listing.objects.all().filter(breeder=breeder_id, is_active=True).count()
    num_sold_listings = Listing.objects.all().filter(breeder=breeder_id, is_active=False).count()
    reviews_list = list(Review.objects.all().filter(reviewed=breeder).order_by("-timestamp"))
    reviews_serialized = [review.serialize() for review in reviews_list]

    paginator = Paginator(reviews_serialized, per_page=3)
    page_num = request.GET.get('page', page_num)
    page = paginator.page(page_num)
    page_objects = page.object_list
    page_has_next = page.has_next()
    page_has_previous = page.has_previous()

    return JsonResponse({
        "breeder": breeder.serialize(), "num_active_listings": num_active_listings, "page_has_next": page_has_next,
        "page_objects": page_objects, "page_num": page_num, "page_has_previous": page_has_previous,
        "num_sold_listings": num_sold_listings, "reviews": [review.serialize() for review in reviews_list]},
        status=201)


@csrf_exempt
def add_review(request, breeder_id):
    """
    Adds review to breeders profile
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    try:
        user = User.objects.get(id=breeder_id)
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with email {breeder_id} does not exist."
        }, status=400)
    review = Review()
    review.reviewer = request.user
    review.reviewed = User.objects.get(id=breeder_id)
    review.content = data.get("content", "")
    review.save()
    return JsonResponse({"message": "Review sent successfully."}, status=201)


@csrf_exempt
def add_to_favorites(request, listing_id, action_name):
    """
    Adds/removes listing from user's favorites
    """
    watchers = request.user
    listing = Listing.objects.get(id=listing_id)
    if(action_name == "+ Favorite"):
        watchers.favorites.add(listing)
    else:
        watchers.favorites.remove(listing)
    return JsonResponse({"message": "Added to favorites successfully."}, status=201)


def add_listing(request):
    """
    Function(form) for breeders to
    add listing
    """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.breeder = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "puppysearch/add_listing.html", {
                "form": form
            })
    else:
        return render(request, "puppysearch/add_listing.html", {
            "form": ListingForm()
        })


@login_required
def delete_listing(request, listing_id):
    """
    Deletes the listing
    """
    listing = Listing.objects.get(pk=listing_id)
    if request.user != listing.breeder:
        return render(request, "puppysearch/error.html", {"message": "You cannot delete someone else's listing!"})
    else:
        listing.delete()
        return HttpResponseRedirect(reverse("my_listings"))


@login_required
def sold_listing(request, listing_id):
    """
    Marks listing as sold
    """
    listing = Listing.objects.get(pk=listing_id)
    if request.user != listing.breeder:
        return render(request, "puppysearch/error.html", {"message": "You cannot mark sold someone else's listing!"})
    else:
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse("my_listings"))


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'price', 'color', 'location']

        def __init__(self, *args, **kwargs):
            super(ListingForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs["class"] = "form-control"


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
            return render(request, "puppysearch/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "puppysearch/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        is_breeder = request.POST.get('is_breeder', False)
        company_name = request.POST.get('company_name', username)
        city = request.POST["city"]
        state = request.POST["state"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if is_breeder == 'on':
            is_breeder = True

            if (not Location.objects.all().filter(city=city).exists()):
                location = Location()
                location.city = city
                location.state = state
                location.save()

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "puppysearch/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.is_breeder = is_breeder
            user.company_name = company_name
            user.save()
        except IntegrityError:
            return render(request, "puppysearch/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "puppysearch/register.html")
