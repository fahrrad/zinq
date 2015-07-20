import site
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from menus.views import menu_items, menu, wait_status, wait, place_order, set_next_timeout
from places.views import orders, order_done, orders_open, order_cancel
from places.views import qr_codes
from places.views import landing
import settings
from website.views import contact


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Uncomment the next line to enable the admin:

                       (r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^$', landing),


                       # QR codes can be encoded more efficiently when they only contain capitals.
                       # see http://code.google.com/p/zxing/wiki/BarcodeContents.
                       # That is why following urls are case insensitive
                       # place order
                       url(r'^order/p/(\w{4,32})/$', place_order),

                       # order done
                       url(r'^order/d/(\w{4,32})/$', order_done),

                       # order cancelled
                       url(r'^order/x/(\w{4,32})/$', order_cancel),

                       # view orders
                       url(r'(?i)^orders/(\w{1,5})/$', orders),

                       # Get open orders (REST call)
                       url(r'^order/o/(\w{1,5})/$', orders_open),

                       # View Menu
                       url(r'^(?i)menu/(\w{4,32})/$', menu),

                       # rest services for the order, to get the menu items
                       url(r'^mi/(\w{4,32})/$', menu_items),

                       #  When ordered, check the wait status here
                       url(r'^wait/(\w{4,32})/$', wait),
                       url(r'^wait_status/(\w{4,32})/$', wait_status),

                       # next timeout setter
                       url(r'^settings/next_timeout/(\d+)$', set_next_timeout),

                       # to get all the QR codes for a place
                       url(r'^qrcodes/([0-9]{1,5})/$', qr_codes),

                       # site specific
                       url(r'^site/$', site, name='site'),
                       url(r'^contact/$', contact, name='contact'),
                       ) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)