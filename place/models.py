from django.db import models
from uuid import uuid4
import menu

class Place(models.Model):
    name = models.CharField(max_length=255)

    # One - One
    menu = models.ForeignKey("menu.Menu", null=True, unique=True)

    def __unicode__(self):
        return self.name

    # Get all orders for this place
    def get_orders(self):
        return list(menu.models.Order.objects.filter(table__place=self).all())


class Table(models.Model):
    # uuid to map to this table
    uuid = models.CharField(max_length=32, default=lambda: uuid4().hex,
                            primary_key=True)

    # place specific identification of tables
    table_nr = models.CharField(max_length=255, blank=True, default="")

    # where is this table located?
    place = models.ForeignKey(Place)

    def get_menu(self):
        """get the menu for a table"""
        return self.place.menu

    def __unicode__(self):
        return "table %s at %s" % (self.table_nr, self.place)
