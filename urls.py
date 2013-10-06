from django.conf.urls import patterns, include, url
from django.contrib import admin

from places.views import welcome, menu, landing, orders, rm_order, wait
from qmenu.views import auth_login, auth_logout

from menus.models import Menu, MenuItem

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

    url(r'^auth_login/$', auth_login, name="auth_login"),
    url(r'^logout/$', auth_logout),

    url(r'^welcome/$', welcome),
    url(r'^menu/(\w{4,32})/$', menu),
    url(r'^MENU/(\w{4,32})/$', "places.views.MENU"),
    url(r'^$', landing),

    # view orders
    url(r'^orders/(\w{1,5})/$', orders),

    # Rest
    url(r'^rest/orders/delete/(\w{4,32})/$', rm_order),

    url(r'^wait/(\w{4,32})/$', wait),
)
