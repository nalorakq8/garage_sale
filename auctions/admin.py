from django.contrib import admin
from .models import Auction,Bid

class AuctionAdmin (admin. ModelAdmin):
    list_display = ('title','seller','starting_bid','created_at')

class BidAdmin (admin. ModelAdmin):
    list_display = ('bidder','amount','bid_at')

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
