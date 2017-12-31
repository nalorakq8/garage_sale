from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^user/(?P<pk>\d+)$', views.profile_view, name='profile_view',),
    url(r'^user/(?P<pk>\d+)/edit$', views.profile_edit, name='profile_edit',),
    url(r'^user/become_seller$', views.become_seller, name='become_seller',),


]
