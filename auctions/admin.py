from django.contrib import admin
from .models import Auction

class AuctionAdmin (admin. ModelAdmin):
    list_display = ('title','seller','starting_bid','created_at','live')

admin.site.register(Auction, AuctionAdmin)
