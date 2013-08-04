from django.db import models
from place.models import Place, Table

from decimal import Decimal


class Menu(models.Model):
    """ An aggregate of MenuItems. """
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name


class MenuItem(models.Model):
    """ A single item on a menu"""

    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=6)
    
    menu = models.ForeignKey(Menu)

    def __unicode__(self):
        return self.name

    class Meta:
        # no menu can contain the same menuitem twice!
        unique_together = ("menu", "name")


class OrderMenuItem(models.Model):
    """ Many to Many mapping table that maps between an order and the menu items that are stored on it.
    This mapping table will also contain a amount, and a price. This is to avoid that if a menu item should
    change after the user placed an order the bill would be different from what was ordered...
    """

    # How many 'things' were ordered
    amount = models.IntegerField(null=False)


    # the total price at the time of the order ( item price * amount)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=6)

    # mapping fields
    menuItem = models.ForeignKey(MenuItem)
    # need a string because the Order model is not yet defined here
    order = models.ForeignKey("Order")


class Order(models.Model):
    """An placed order. This contains a reference to who placed the order, and
    where it was placed. Also contains a list of things that were ordered, and
    an order status

    The lifecycle of an order:

    ordered -> done -> payed

    """

    # the status a order can be in
    ORDERED = 'OR'
    DONE = 'DO'
    PAYED = 'PA'

    ORDER_STATUSES = (
        (ORDERED, 'Ordered'),
        (DONE, 'Done'),
        (PAYED, 'Payed'),
    )

    # the table that ordered
    table = models.ForeignKey(Table)
    menuItems = models.ManyToManyField(MenuItem, through=OrderMenuItem)

    # the status of the order ( ordered -> done -> payed)
    # to display the status user friendly, use
    # self.get_status_display()
    status = models.CharField(max_length=2, choices=ORDER_STATUSES,
                              default=ORDERED)

    def addItem(self, menuItem, amount):
        """ add amount menuitems to the order. Will also add the total
        price to the total
        """

        price = amount * menuItem.price

        orderMenuItem = OrderMenuItem(menuItem=menuItem, order=self,
                                      amount=amount, price=price)

        orderMenuItem.save()

    def calculate_total_price(self):
        total = Decimal('0')

        for orderMenuItem in OrderMenuItem.objects.filter(order=self).all():
            total += orderMenuItem.price

        return total

    def proceed(self):
        if self.status == self.ORDERED:
            self.status = self.DONE

        elif self.status == self.DONE:
            self.status = self.PAYED

        else:
            raise Exception('Cannot proceed. Item is payed')






    


