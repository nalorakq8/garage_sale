from django.contrib import admin
from .models import User,Seller,CustomerSupport,Accountant


class UserAdmin (admin. ModelAdmin):
    list_display = ('name', 'email', 'phone_number', "user",'address')

class SellerAdmin (admin. ModelAdmin):
    list_display = ('user','cvv_number','card_holder_name','card_number')

class CustomerSupportAdmin (admin. ModelAdmin):
    list_display = ('user',)

class AccountantAdmin (admin. ModelAdmin):
    list_display = ('user',)

admin.site.register(User, UserAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(CustomerSupport, CustomerSupportAdmin)
admin.site.register(Accountant, AccountantAdmin)
