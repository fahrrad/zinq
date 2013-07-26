from django.db import models
from uuid import uuid4


class Place(models.Model):
    name = models.CharField(max_length=255)
    menu = models.ForeignKey("menu.Menu", null=True)

    def __unicode__(self):
        return self.name

class Table(models.Model):
    # uuid to map to this table
    uuid = models.CharField(max_length=32, default=lambda : uuid4().hex, primary_key=True)

    # where is this table located?
    place = models.ForeignKey(Place)

    def get_menu(self):
        """get the menu for a table"""
        return self.place.menu

