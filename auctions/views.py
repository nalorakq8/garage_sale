from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404
from .forms import NewAuctionForm, NewBidForm, EditAuctionForm, PaymentForm, TicketForm
from .models import Auction, Bid, Ticket, Payment
from django.core.urlresolvers import reverse
from datetime import datetime
from django.db.models import Q
from django.core.mail import EmailMessage
from django.utils import timezone
from django.core.exceptions import ValidationError


def send_emails():
    auctions = Auction.objects.filter(
        Q(ending_at__lte=datetime.now()) & Q(email_sent=False))
    if auctions:
        for auction in auctions:
            if len(Bid.objects.filter(auction=auction.pk)) > 0:
                highest_bid = Bid.objects.filter(
                    auction=auction.pk).order_by('-amount')[0]
                email = EmailMessage(
                    'Congratz {} you have won the {} auction'.format(
                        highest_bid.bidder.name, auction.title),
                    """Hello {}, you have won the {} auction click the following link for the payment
http://127.0.0.1:8000{}""".format(highest_bid.bidder.name, auction.title, reverse('payment', kwargs={
                        'pk': auction.pk, })),

                    to=[highest_bid.bidder.email])
                email.send()
                auction.email_sent = True
                auction.save()
        else:
            pass


@login_required
def payment(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    highest_bid = Bid.objects.filter(auction=auction.pk).order_by('-amount')[0]
    if auction.payed == False and auction.ending_at < timezone.now() and highest_bid.bidder.pk == request.user.user.pk:
        highest_bid = Bid.objects.filter(
            auction=auction.pk).order_by('-amount')[0]
        if request.method == 'POST':
            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Payment was successfully accepted.')
                email = EmailMessage(
                    'Payment confirmation for {} auction'.format(
                        auction.title),
                    """Hello {}, Your payment has been recivied for {} auction, Amount {}KD""".format(highest_bid.bidder.name, auction.title, highest_bid.amount), to=[highest_bid.bidder.email])
                email.send()
                email = EmailMessage(
                    'Payment for {}'.format(auction.title),
                    """Dear {}, A payment has been recivied for {} auction, from {},
please contact him for shipping information,
buyer email {}""".format(auction.seller.user.name, auction.title, highest_bid.bidder.name, highest_bid.bidder.email), to=[auction.seller.user.email])
                email.send()
                auction.payed = True
                auction.save()
                return redirect(reverse('home'))
        else:

            form = PaymentForm(initial={'bid': highest_bid.pk,
                                        })

        return render(
            request,
            'payment.html',
            {
                "auction": auction,
                "highest_bid": highest_bid,
                "form": form
            }
        )
    else:
        raise Http404


@login_required
def auction_create(request):
    send_emails()
    if not hasattr(request.user.user, 'seller'):
        raise Http404
    if request.method == 'POST':
        form = NewAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Auction was successfully created.')
            return redirect(reverse('my_auctions'))
    else:

        form = NewAuctionForm(initial={'seller': request.user.user.seller.pk,
                                       })

    return render(
        request,
        'create_auction.html',
        {
            "form": form,
        }
    )


def auction_view(request, pk):
    send_emails()
    qs = get_object_or_404(Auction, pk=pk)
    if qs.ending_at < timezone.now():
        raise Http404
    bid = Bid.objects.filter(auction=pk).order_by('-amount')
    recomendations = Auction.objects.filter(category=qs.category)
    recomendations = recomendations.exclude(pk=qs.pk).order_by('?')[:4]
    if bid:
        bid = bid[0]
    else:
        bid = None
    return render(
        request,
        'auction_view.html',
        {
            'auction': qs,
            'bid': bid,
            'recomendations': recomendations
        })


@login_required
def create_bid(request, pk):
    send_emails()
    qs = Auction.objects.get(pk=pk)
    bid = Bid.objects.filter(auction=pk).order_by('-amount')
    if bid:
        bid = bid[0]
        min_bid = bid.amount + 1
    else:
        bid = None
        min_bid = qs.starting_bid + 1

    if request.user.user == qs.seller.user:
        messages.error(request, "You can't bid on your own auction")
        return redirect(reverse('auction_view', kwargs={
            'pk': pk, }))

    if request.method == 'POST':
        form = NewBidForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Your bid has been submitted')
            return redirect(reverse('auction_view', kwargs={
                'pk': pk, }))
    else:

        form = NewBidForm(
            initial={'auction': [pk, ], 'bidder': request.user.user.pk})
    return render(
        request,
        'create_bid.html',
        {
            'min_bid': min_bid,
            'bid': bid,
            'auction': qs,
            'form': form,
            'pk': pk
        })


def view_auctions_list(request):
    send_emails()
    auctions = Auction.objects.filter(ending_at__gte=datetime.now())[:10]
    return render(
        request,
        'view_auctions_list.html',
        {
            'auctions': auctions,
        })


def view_latest_auctions_list(request):
    send_emails()
    auction_obj = Auction.objects.filter(ending_at__gte=datetime.now())
    auctions = auction_obj.order_by('-created_at')[:4]
    trending = auction_obj.annotate(num_bids=Count('bid')).filter(
        num_bids__gt=0).order_by('-num_bids')[:5]
    return render(
        request,
        'index.html',
        {
            'auctions': auctions,
            'trending': trending,
        })


@login_required
def my_auctions(request):
    send_emails()
    if not hasattr(request.user.user, 'seller'):
        raise Http404
    auctions = Auction.objects.filter(seller=request.user.user.seller)
    return render(
        request,
        'my_auctions.html',
        {
            'auctions': auctions,
        })


@login_required
def auction_edit(request, pk):
    send_emails()
    auction = get_object_or_404(Auction, pk=pk)
    if auction.seller.user.pk == request.user.user.pk:
        if request.method == 'POST':
            auction_form = EditAuctionForm(
                request.POST, request.FILES, instance=auction)
            if auction_form.is_valid():
                obj = auction_form.save()
                messages.success(request, 'Auction was successfully updated.')
                return redirect(reverse('auction_view', kwargs={
                    'pk': pk, }))
        else:
            auction_form = EditAuctionForm(instance=auction)
        return render(
            request,
            'auction_edit.html',
            {
                "form": auction_form,
                'pk': pk,
            }
        )
    else:
        raise Http404


@login_required
def auction_delete(request, pk):
    send_emails()
    auction = get_object_or_404(Auction, pk=pk)
    if request.user.user == auction.seller.user:
        auction.delete()
        messages.success(request, 'Auction was successfully deleted.')
        return redirect(reverse('my_auctions'))
    else:
        raise Http404


def auction_search(request):
    send_emails()
    if request.method == 'GET':
        auction = request.GET.get('search')
        category = request.GET.get('category')
        auctions = Auction.objects.filter(ending_at__gte=datetime.now())
        if category != "":
            auctions = auctions.filter(category=category)
            auctions = auctions.filter(
                Q(title__icontains=auction) | Q(description__icontains=auction))
        else:
            auctions = auctions.filter(
                Q(title__icontains=auction) | Q(description__icontains=auction))
        return render(request, "view_auctions_list.html", {"auctions": auctions})
    else:
        return render(request, "view_auctions_list.html", {})

def contact_us(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket was successfully Submitted.')
            return redirect(reverse('home'))
    else:
        if hasattr(request.user, 'user') :
            form = TicketForm(initial={'user': request.user.user.pk,
                                        'email': request.user.user.email,
                                        'phone_number': request.user.user.phone_number,
                                        'name': request.user.user.name
                                       })
        else:
            form = TicketForm()
    return render(
        request,
        'contact_us.html',
        {
            "form": form,
        }
    )
@login_required
def view_tickets_list(request):
    if hasattr(request.user.user, 'customersupport'):
        tickets = get_list_or_404(Ticket,replyed=False)
        return render(
            request,
            'view_tickets_list.html',
            {
                "tickets": tickets,
            }
        )
    else:
        raise Http404

def reply_ticket(request,pk):
    if hasattr(request.user.user, 'customersupport'):
        ticket= get_object_or_404(Ticket,pk=pk)
        if request.method == 'POST' and request.POST.get('message') != "":
            message = request.POST.get('message')
            email = EmailMessage(
                'RE: {}'.format(
                    ticket.subject),
                """{}""".format(message), to=[ticket.email])
            email.send()
            ticket.replyed=True
            ticket.save()
            messages.success(request, 'Ticket was successfully closed.')
            return redirect(reverse('view_tickets_list'))
        return render(
            request,
            'reply_ticket.html',
            {
                "ticket": ticket,
            }
        )
    else:
        raise Http404
@login_required
def books(request):
    if hasattr(request.user.user, 'accountant'):
        if Auction.objects.filter(payed = True):
            auctions = get_list_or_404(Auction,payed=True)
            payments = get_list_or_404(Payment)
            profit = 0.0
            number_of_auctions = 0
            data = {"January":0, "February":0, "March":0, "April":0, "May":0, "June":0, "July":0,"August":0, "September":0,"October":0,"November":0,"December":0}
            data_list = []
            for auction in auctions:
                number_of_auctions += 1
            for payment in payments:
                profit = profit + round((float(payment.bid.amount) * 0.1),2)
                print(payment.payed_at.date())
                data[payment.payed_at.date().strftime('%B')]+=round((float(payment.bid.amount) * 0.1),2)
            for key,value in data.items():
                data_list.append(value)
        else:
            auctions = None
            profit=None
            number_of_auctions = None
            data_list = [0,0,0,0,0,0,0,0,0,0,0,0]
        return render(request,
        'books.html',
        {
            "auctions": auctions,
            "profit": profit,
            "number_of_auctions": number_of_auctions,
            'data': data_list
        })
    else:
        raise Http404
