from django.contrib import admin

from .models import User, Color, Listing, Location, Review
# Register your models here.

admin.site.register(User)
admin.site.register(Color)
admin.site.register(Listing)
admin.site.register(Location)
admin.site.register(Review)
