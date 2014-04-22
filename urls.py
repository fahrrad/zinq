from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from menus.views import menu_items, menu
from orders.views import wait, orders, rm_order, place_order, wait_status
from places.views import qr_codes
from places.views import welcome, landing
import settings


admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^welcome/$', welcome),
    url(r'^menu/(\w{4,32})/$', menu),

     # QR codes can be encoded more efficiently when they only contain capitals.
     #
     # see http://code.google.com/p/zxing/wiki/BarcodeContents
    url(r'^MENU/(\w{4,32})/$', menu),
    url(r'^$', landing),

    # view orders
    url(r'^orders/(\w{1,5})/$', orders),

    # place order
    url(r'^orders/p/(\w{4,32})/$', place_order),

    # rest services for the order
    url(r'^mi/(\w{4,32})/$', menu_items),

    # Rest
    url(r'^rest/orders/delete/(\w{4,32})/$', rm_order),

    url(r'^wait/(\w{4,32})/$', wait),
    url(r'^wait_status/(\w{4,32})/$', wait_status),
    url(r'^qrcodes/([0-9]{1,5})/$', qr_codes),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)