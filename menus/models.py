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

    description = models.CharField(max_length=1024, blank=True, null=True)

    position = models.PositiveSmallIntegerField("Position")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.position is None:
            try:
                last = model.objects.filter(category=self.category).order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                # First Row
                self.position = 0
        return super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        # no menus can contain the same menu item twice!
        unique_together = ("menu", "name")
        verbose_name_plural = "Producten"
        verbose_name = "Product"
        ordering = ['position']