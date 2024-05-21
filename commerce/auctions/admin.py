from django.contrib import admin

from .models import Listing, Category, Bid, Comment, WatchList

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)