from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("colors", views.colors, name="colors"),
    path("colors/<int:color_id>", views.show_color_listings, name="show_color_listings"),
    path("profile/<int:breeder_id>/<int:page_num>", views.profile, name="profile"),
    path("breeders", views.breeders, name="breeders"),
    path("breeders_listings/<int:breeder_id>", views.show_breeder_listings, name="show_breeder_listings"),
    path("locations", views.locations, name="locations"),
    path("locations/<int:location_id>", views.show_location_listings, name="show_location_listings"),
    path("add_review/<int:breeder_id>", views.add_review, name="add_review"),
    path("add_to_favorites/<int:listing_id>/<str:action_name>", views.add_to_favorites, name="add_to_favorites"),
    path("favorites", views.show_favorites, name="show_favorites"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_reviews", views.my_reviews, name="my_reviews"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("sold/<int:listing_id>", views.sold_listing, name="sold_listing"),
    path("search", views.search, name="search")
]
