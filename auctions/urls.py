from django.conf.urls import url
from auctions import views

urlpatterns = [
    url(r'^auction/create/$', views.auction_create,
        name='auction_create'),
    url(r'^auction/(?P<pk>\d+)$', views.auction_view, name='auction_view',),
    url(r'^auction/list$', views.view_auctions_list, name='view_auctions_list',),
    url(r'^auction/(?P<pk>\d+)/bid$', views.create_bid, name='create_bid',),
]
