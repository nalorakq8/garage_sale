from django.db import models
from users.models import Seller, User

class Bid(models.Model):
    bidder = models.ForeignKey(User, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_at = models.DateTimeField(auto_now_add=True)

class Auction(models.Model):
    title = models.CharField(max_length=240)
    seller = models.ForeignKey(Seller, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    bids = models.ManyToManyField(Bid, through='AuctionBid')
    created_at = models.DateTimeField(auto_now_add=True)
    live = models.BooleanField(default=False)

class AuctionBid(models.Model):
    auction = models.ForeignKey(Auction)
    bid = models.ForeignKey(Bid)
