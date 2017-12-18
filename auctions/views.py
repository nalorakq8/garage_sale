from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404
from .forms import NewAuction
from .models import Auction
# Create your views here.


@login_required
def auction_create(request):
    if not request.user.user.seller:
        raise Http404
    if request.method == 'POST':
        form = NewAuction(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect('/')
    else:

        form = NewAuction(initial={'seller': request.user.user.seller.pk,
                                   'bids': None,
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
    return render(
        request,
        'auction_view.html',
        {
            'auction': qs,
        })


def view_auctions_list(request):
    return


def delete_auction(request):
    return
