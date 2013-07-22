from django.conf.urls import patterns, include, url
from django.contrib import admin
from place.views import welcome, menu

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

    url(r'welcome/', welcome),
    url(r'menu/(\w{4,32})', menu)
)
