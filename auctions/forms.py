from django import forms
from .models import Auction

class NewAuction(forms.ModelForm):

    class Meta:
        model = Auction
        exclude =['bids']
        widgets = {
            'seller': forms.HiddenInput,
        }
