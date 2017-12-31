from django.contrib import admin
from .models import Auction, Bid, Payment, Ticket


class AuctionAdmin (admin. ModelAdmin):
    list_display = ('title', 'seller', 'starting_bid',
                    'created_at', 'ending_at')


class BidAdmin (admin. ModelAdmin):
    list_display = ('bidder', 'amount', 'bid_at', 'auction_title')

    def auction_title(self, obj):
        return "\n".join([a.title for a in obj.auction.all()])


class PaymentAdmin (admin. ModelAdmin):
    list_display = ('auction_title', 'payment_method', 'payed_at')

    def payment_method(self, obj):
        return "\n".join([a for a in obj.method.all()])

    def auction_title(self, obj):
        return "\n".join([a.title for a in obj.bid.auction.all()])


class TicketAdmin(admin. ModelAdmin):
    list_display = ('name', 'email', 'subject','replyed')


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Ticket, TicketAdmin)
