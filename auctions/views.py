from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404
from .forms import NewAuction,NewBid
from .models import Auction,Bid
from django.core.urlresolvers import reverse
from datetime import datetime


@login_required
def auction_create(request):
    if not hasattr(request.user.user,'seller'):
        raise Http404
    if request.method == 'POST':
        form = NewAuction(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('/')
    else:

        form = NewAuction(initial={'seller': request.user.user.seller.pk,
                                   })

    return render(
        request,
        'create_auction.html',
        {
            "form": form,
        }
    )


def auction_view(request,pk):
    qs = Auction.objects.get(pk=pk)
    bid =Bid.objects.filter(auction=pk).order_by('-amount')
    if bid:
        bid=bid[0]
    else:
        bid=None
    return render(
        request,
        'auction_view.html',
        {
            'auction': qs,
            'bid': bid,
        })
@login_required
def create_bid(request,pk):
    qs = Auction.objects.get(pk=pk)
    bid=Bid.objects.filter(auction=pk).order_by('-amount')
    if bid:
        bid=bid[0]
        min_bid=bid.amount + 1
    else:
        bid=None
        min_bid=qs.starting_bid + 1

    if request.user.user == qs.seller.user:
        messages.error(request, "You can't bid on your own auction")
        return redirect(reverse('auction_view', kwargs={
            'pk': pk,}))

    if request.method == 'POST':
        form = NewBid(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Your bid has been submitted')
            return redirect(reverse('auction_view', kwargs={
                'pk': pk,}))
    else:

        form = NewBid(initial={'auction':[pk,],'bidder': request.user.user.pk})
    return render(
        request,
        'create_bid.html',
        {
            'min_bid':min_bid,
            'bid':bid,
            'auction':qs,
            'form':form,
            'pk':pk
        })

def view_auctions_list(request):
    auctions = Auction.objects.filter(ending_at__gte=datetime.now())[:10]
    return render(
        request,
        'view_auctions_list.html',
        {
            'auctions': auctions,
        })

def view_latest_auctions_list(request):
    auctions = Auction.objects.order_by('created_at')[:4]
    trending = Auction.objects.annotate(num_bids=Count('bid')).filter(num_bids__gt=0).order_by('-num_bids')[:5]
    return render(
        request,
        'index.html',
        {
            'auctions': auctions,
            'trending':trending,
        })

def delete_auction(request):
    return

def send_emails(request):
    print('hi')
    return
