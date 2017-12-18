from django.contrib import admin
from .models import User,Seller


class UserAdmin (admin. ModelAdmin):
    list_display = ('name', 'email', 'phone_number', "user",'address')

class SellerAdmin (admin. ModelAdmin):
    list_display = ('user','cvv_number','card_holder_name','card_number')

admin.site.register(User, UserAdmin)
admin.site.register(Seller, SellerAdmin)
