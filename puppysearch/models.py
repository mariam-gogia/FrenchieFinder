from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    company_name = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    is_breeder = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now)
    favorites = models.ManyToManyField('Listing', blank=True, related_name="watchers")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "company_name": self.company_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
        }


class Color(models.Model):
    class Meta:
        verbose_name_plural = "colors"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=225)
    state = models.CharField(max_length=64)

    def __str__(self):
        return self.city + ", " + self.state


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=datetime.now, null=True, blank=True)
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="reviewed")

    def serialize(self):
        return {
            "id": self.id,
            "reviewer": self.reviewer.serialize(),
            "content": self.content,
            "reviewed": self.reviewed.serialize(),
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
        }


class Listing(models.Model):
    breeder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=32)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="listings")
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
