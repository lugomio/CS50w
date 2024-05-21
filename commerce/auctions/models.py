from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)

    def __str__(self):
        return f"Category {self.id} - {self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.FloatField()
    banner = models.URLField(max_length=256, blank=True, null=True, editable=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True, editable=True)
    active = models.BooleanField(default=True, blank=False, null=False, editable=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winn_listings", blank=True, null=True, editable=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateField(auto_now=True, blank=False, null=False, editable=True)

    def __str__(self):
        return f"Listing {self.id} - {self.title} (Created by: {self.created_by})"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid {self.id} - ${self.price} (Bidder: {self.bidder})"

class Comment(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment {self.id} - {self.comment} (Autor: {self.autor})"
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_items")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
    
    def __str__(self):
        return f"WatchList ({self.user} - {self.listing.title})"