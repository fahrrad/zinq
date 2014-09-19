import logging
from uuid import uuid4

from django.db import models



# Create your models here.
from menus.models import MenuItem
from places.models import Table


logger = logging.getLogger(__name__)


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

    def add_menuitem(self, menuItem, amount):
        """ add amount menuitems to the orders. Will also add the total
        price to the total
        """

        price = amount * menuItem.price

        order_menuitem = OrderMenuItem(menuItem=menuItem, order=self,
                                       amount=amount, price=price)

        order_menuitem.save()

    def add_item_by_pk(self, menu_item_pk, amount):
        """add a menu item to this order. Fetches it by its PK. Adds @amount times."""
        try:
            mi = MenuItem.objects.get(pk=menu_item_pk)
            price = int(amount) * mi.price
            order_menu_item = OrderMenuItem(menuItem=mi, order=self,
                                            amount=amount, price=price)

            order_menu_item.save()

        except MenuItem.DoesNotExist as mi_doesnotexist:
            logger.warn("trying to get an unexistsing menuitem (id %d) " % menu_item_pk)

    def calculate_total_price(self):
        return sum([omi.price for omi in OrderMenuItem.objects.filter(order=self)])

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
                                      ordermenuitem.amount, str(ordermenuitem.price)))

        return menuitems_amounts


class OrderLineTransferObject():
    """represents one line in an order that will be sent to the server"""

    def __init__(self, menu_item_uuid, amount):
        self.menu_item_uuid = menu_item_uuid
        self.amount = amount


class OrderTransferObject():
    """This object will be serialised on the client, and sent to the server"""

    def __init__(self, uuid, table_uuid, order_line_list):
        self.uuid = uuid
        self.table_uuid = uuid
        self.order_line_list = order_line_list