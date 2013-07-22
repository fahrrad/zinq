from django.db import models

class Menu(models.Model):
    """ An aggregate of MenuItems. """
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class MenuItem(models.Model):
    """ A single item on a menu"""

    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.FloatField()
    
    menu = models.ForeignKey(Menu)

    def __unicode__(self):
        return self.name

    


