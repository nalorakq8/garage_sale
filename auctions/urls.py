from django.conf.urls import url
from auctions import views
urlpatterns = [
    url(r'^auction/create/$', views.auction_create,
        name='auction_create'),
    url(r'^auction/(?P<pk>\d+)$', views.auction_view, name='auction_view',),
    url(r'^auction/list$', views.view_auctions_list, name='view_auctions_list',),
    url(r'^auction/(?P<pk>\d+)/bid$', views.create_bid, name='create_bid',),
    url(r'^auction/my_auctions$', views.my_auctions, name='my_auctions',),
    url(r'^auction/(?P<pk>\d+)/edit$', views.auction_edit, name='auction_edit',),
    url(r'^auction/(?P<pk>\d+)/delete$', views.auction_delete, name='auction_delete',),
    url(r'^auction/(?P<pk>\d+)/pay$', views.payment, name='payment',),
    url(r'^auction/list/search$',
        views.auction_search, name="auction_search",),
]
