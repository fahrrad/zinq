from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

import orders


class Place(models.Model):
    name = models.CharField(max_length=255)

    # owner
    user = models.ForeignKey(User,  null=True)

    # One - One
    menu = models.ForeignKey("menus.Menu", null=True, unique=True)

    def __unicode__(self):
        return self.name

    # Get all orders for this places
    def get_orders(self):
        return list(orders.models.Order.objects.filter(table__place=self,
                                                       status=orders.models.Order.ORDERED).all())


class Table(models.Model):
    # uuid to map to this table
    uuid = models.CharField(max_length=32, default=lambda: uuid4().hex,
                            primary_key=True)

    # places specific identification of tables
    table_nr = models.CharField(max_length=255, blank=True, default="")

    # where is this table located?
    place = models.ForeignKey(Place)

    def get_menu(self):
        """get the menus for a table"""
        return self.place.menu

    def __unicode__(self):
        return "table %s at %s" % (self.table_nr, self.place)
