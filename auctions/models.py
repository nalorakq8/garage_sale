from django.db import models
from users.models import Seller, User
from PIL import Image
from io import BytesIO
from users.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext as _
import sys


class Auction(models.Model):
    CATEGORIES = (("Mobiles", "Mobiles"),
                  ("Computers", "Computers"),
                  ("Automobiles", "Automobiles"),
                  ("Antiques", "Antiques"))
    title = models.CharField(max_length=240)
    seller = models.ForeignKey(Seller, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    ending_at = models.DateTimeField()
    description = models.CharField(
        max_length=1200, null=False, blank=False, default="")
    picture = models.FileField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    category = models.CharField(
        "category", null=False, choices=sorted(CATEGORIES), max_length=64)

    def clean(self):
        if self.picture:
            file = self.picture.name
            filetype = file.split('.')[-1]
            if filetype not in ["jpg", "jpeg", "png", "gif", ]:
                raise ValidationError("Please upload a picture not {} file.".format(filetype))

        if self.ending_at < timezone.now():
            raise ValidationError(
                _('Auction ending date and time must be later than now.'))
        return self.picture

    def get_absolute_url(self):
        return reverse('auction_view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{}-{}".format(self.title, self.seller)

    def __str__(self):
        return "{}-{}".format(self.title, self.seller)

    def save(self):
        if self.picture:
            # Opening the uploaded image
            w, h = get_image_dimensions(self.picture)
            aspect_ratio = float(w) / float(h)

            im = Image.open(self.picture)
            output = BytesIO()
            output2 = BytesIO()
            im = im.resize((700, 300))

            # after modifications, save it to the output
            im.save(output, format='png', quality=100)
            output.seek(0)
            output2.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.picture = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.picture.name.split(
                '.')[0], 'image/png', sys.getsizeof(output), None)

        super(Auction, self).save()


class Bid(models.Model):
    bidder = models.ForeignKey(User, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_at = models.DateTimeField(auto_now_add=True)
    auction = models.ManyToManyField(Auction)

    def __unicode__(self):
        return u"{}-{}".format(self.bidder, self.auction)

    def __str__(self):
        return "{}-{}".format(self.bidder, self.auction)

class Payment(models.Model):
    METHODS = (('Paypal','Paypal'),
                ('Credit/Debit Card','Credit/Debit Card'))
    bid = models.OneToOneField(Bid)
    payment_method = models.CharField(
        "method", null=False, choices=sorted(METHODS), max_length=64)
    payed_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    message = models.CharField(max_length=3000)
    subject = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=False)
    replyed = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True,blank=True)
