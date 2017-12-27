from django import forms
from .models import Auction,Bid
from datetimewidget.widgets import DateTimeWidget
class NewAuction(forms.ModelForm):

    class Meta:
        model = Auction
        fields='__all__'
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': True,
            'showMeridian': True}
        widgets = {
            #'seller': forms.HiddenInput,
            'ending_at': DateTimeWidget(options=dateTimeOptions,
                                        usel10n=True, bootstrap_version=3),
        }
class NewBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields='__all__'
        widgets = {
            #'bidder': forms.HiddenInput,
            #'auction':forms.HiddenInput,
        }
