from decimal import Decimal
from uuid import uuid4
from django.db import models

# Create your models here.
from menus.models import MenuItem
from place.models import Table


class OrderMenuItem(models.Model):
    """ Many to Many mapping table that maps between an orders and the menus items that are stored on it.
    This mapping table will also contain a amount, and a price. This is to avoid that if a menus item should
    change after the user placed an orders the bill would be different from what was ordered...
    """

    # How many 'things' were ordered
    amount = models.IntegerField(null=False)


    # the total price at the time of the orders ( item price * amount)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=6)

    # mapping fields
    menuItem = models.ForeignKey(MenuItem)
    # need a string because the Order model is not yet defined here
    order = models.ForeignKey("Order")


class Order(models.Model):
    """An placed orders. This contains a reference to who placed the orders, and
    where it was placed. Also contains a list of things that were ordered, and
    an orders status

    The lifecycle of an orders:

    ordered -> done -> payed

    """

    # the status a orders can be in
    ORDERED = 'OR'
    DONE = 'DO'
    PAYED = 'PA'

    ORDER_STATUSES = (
        (ORDERED, 'Ordered'),
        (DONE, 'Done'),
        (PAYED, 'Payed'),
    )
    # generated pk
    uuid = models.CharField(max_length=32, default=lambda: uuid4().hex,
                            primary_key=True)

    # the table that ordered
    table = models.ForeignKey(Table)
    menuItems = models.ManyToManyField(MenuItem, through=OrderMenuItem)

    # the status of the orders ( ordered -> done -> payed)
    # to display the status user friendly, use
    # self.get_status_display()
    status = models.CharField(max_length=2, choices=ORDER_STATUSES,
                              default=ORDERED)

    def addItem(self, menuItem, amount):
        """ add amount menuitems to the orders. Will also add the total
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


    def get_menuitems_amounts(self):
        """returns a list of tuples, containing the menuitem name, and the ordered amount"""

        menuitems_amounts = []
        for ordermenuitem in self.ordermenuitem_set.all():
            menuitems_amounts.append((ordermenuitem.menuItem.name,
                                        ordermenuitem.amount))

        return menuitems_amounts
