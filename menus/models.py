from django.db import models


class Menu(models.Model):
    """ An aggregate of MenuItems. """
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name


class MenuItem(models.Model):
    """ A single item on a menus"""
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=6)
    
    menu = models.ForeignKey(Menu)

    def __unicode__(self):
        return self.name

    class Meta:
        # no menus can contain the same menuitem twice!
        unique_together = ("menu", "name")








    


