from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=False, default="")
    address = models.CharField(max_length=240)

    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)


class Seller(models.Model):
    user = models.OneToOneField(User)
    card_number = models.CharField(max_length=19)
    cvv_number = models.CharField(max_length=3)
    card_holder_name = models.CharField(max_length=240)
    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{}".format(self.user.name)

    def __str__(self):
        return "{}".format(self.user.name)

class Customer_support(models.Model):
    user = models.OneToOneField(User)


class Accountant(models.Model):
    user = models.OneToOneField(User)
