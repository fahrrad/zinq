from django.conf.urls import patterns, include, url
from django.contrib import admin
from place.views import welcome, menu, landing, orders, rm_order, wait, qr_codes
from rest_framework import viewsets, routers
from menu.models import Order, Menu, MenuItem


class OrderViewSets(viewsets.ModelViewSet):
    model = Order

class MenuViewSet(viewsets.ModelViewSet):
    model = Menu

class MenuItemsViewSet(viewsets.ModelViewSet):
    model = MenuItem

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSets)
router.register(r'menus', MenuViewSet)
router.register(r'menuitems', MenuItemsViewSet)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
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
    url(r'^MENU/(\w{4,32})/$', "place.views.MENU"),
    url(r'^$', landing),

    # view orders
    url(r'^orders/(\w{1,5})/$', orders),

    # Rest
    url(r'^rest/orders/delete/(\w{4,32})/$', rm_order),

    url(r'^rest/', include(router.urls)),
    url(r'^rest/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^wait/(\w{4,32})/$', wait),

    url(r'^qrcodes/([0-9]{1,5})/$', qr_codes),
                       
)
