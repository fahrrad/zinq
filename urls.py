from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from orders.models import Order
from places.views import welcome, menu, landing, orders, rm_order, wait, qr_codes
from rest_framework import viewsets, routers
from menus.models import Menu, MenuItem

from places.views import welcome, menu, landing, orders, rm_order, wait

from menus.models import Menu, MenuItem

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
import settings

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qmenu.views.home', name='home'),
    # url(r'^qmenu/', include('qmenu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^welcome/$', welcome),
    url(r'^menu/(\w{4,32})/$', menu),
    url(r'^MENU/(\w{4,32})/$', "places.views.MENU"),
    url(r'^$', landing),

    # view orders
    url(r'^orders/(\w{1,5})/$', orders),

    # Rest
    url(r'^rest/orders/delete/(\w{4,32})/$', rm_order),

    url(r'^rest/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^wait/(\w{4,32})/$', wait),
    url(r'^qrcodes/([0-9]{1,5})/$', qr_codes),
                       
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)