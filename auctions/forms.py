from django import forms
from .models import Auction,Bid, Payment, Ticket
from datetimewidget.widgets import DateTimeWidget
from datetime import datetime
class NewAuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields='__all__'
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': True,
            'showMeridian': True,
            'startDate': str(datetime.now().date())}
        widgets = {
            #'seller': forms.HiddenInput,
            'ending_at': DateTimeWidget(options=dateTimeOptions,
                                        usel10n=True, bootstrap_version=3),
        }
class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields='__all__'
        widgets = {
            #'bidder': forms.HiddenInput,
            #'auction':forms.HiddenInput,
        }


class EditAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields='__all__'
        widgets ={
        'description':forms.Textarea(),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields='__all__'

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields='__all__'
