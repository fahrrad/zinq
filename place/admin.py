__author__ = 'ward'

from django.contrib import admin
from place.models import Table, Place

admin.site.register(Place)
admin.site.register(Table)

