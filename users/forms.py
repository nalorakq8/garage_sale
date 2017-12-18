from .models import User
from django import forms

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
        'user' : forms.HiddenInput,
        }

    def signup(self, request, user):
        User.objects.create(
            user=user,
            name=user.username,
            email=user.email,
            address=self.cleaned_data.get('address'),
            phone_number=self.cleaned_data.get('phone_number')
        )
