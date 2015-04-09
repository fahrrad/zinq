from django.db import models


class Menu(models.Model):
    """ An aggregate of MenuItems. """
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    """A category of Menu Items. For example: Beer, Sandwiches... A category should be unique per place,
    because the owner of a place will want to select only the categories he created.

    In a future version, categories could get translations, so when people enter products, categories can
    be automatically proposed"""

    from places.models import Place

    name = models.CharField(max_length=255, blank=False, null=False)
    place = models.ForeignKey(Place)

    class Meta:
        unique_together = ("name", "place")


class MenuItem(models.Model):
    """ A single item on a menus"""
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=6)

    category = models.CharField(max_length=255)

    menu = models.ForeignKey(Menu)

    def __str__(self):
        return self.name

    class Meta:
        # no menus can contain the same menu item twice!
        unique_together = ("menu", "name")