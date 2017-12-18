from django.conf.urls import url
from auctions import views

urlpatterns = [
    url(r'^auction/create/$', views.auction_create,
        name='auction_create'),
    url(r'^auction/(?P<pk>\d+)$', views.auction_view, name='auction_view',),
]
