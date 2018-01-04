"""garage_sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from auctions import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls',)),
    url(r'^auctions/', include('auctions.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^contact_us/$',views.contact_us,name='contact_us'),
    url(r'^tickets/$',views.view_tickets_list,name='view_tickets_list'),
    url(r'^tickets/(?P<pk>\d+)$',views.reply_ticket,name='reply_ticket'),
    url(r'^books/$',views.books,name='books'),
    url(r'^term_of_use/$',TemplateView.as_view(template_name='term_of_use.html')),
    url(r'^$',views.view_latest_auctions_list,name='home')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
