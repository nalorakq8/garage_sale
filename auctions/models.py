from django.db import models
from users.models import Seller, User
from PIL import Image
from io import BytesIO
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import get_image_dimensions
import sys

class Auction(models.Model):
    title = models.CharField(max_length=240)
    seller = models.ForeignKey(Seller, blank=True,null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    ending_at = models.DateTimeField()
    description = models.CharField(max_length=1200,null=False,blank=False,default="")
    picture = models.ImageField(null=True,blank=True)
    email_sent = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('auction_view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{}-{}".format(self.title,self.seller)

    def __str__(self):
        return "{}-{}".format(self.title,self.seller)

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
        return u"{}-{}".format(self.bidder,self.auction)

    def __str__(self):
        return "{}-{}".format(self.bidder,self.auction)
