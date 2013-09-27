"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import logging
from decimal import Decimal

from django.test import TestCase
from menu import services
from menu.models import MenuItem, Menu
from menu.services import place_order
from order.models import Order
from place.models import Place, Table


# integration testing
from django.test.client import Client

logger = logging.getLogger(__name__)


class MenuTest(TestCase):
    """ Simple tests on the MenuItem object, and there menu group """

    def setUp(self):
        """create some stuff"""
        self.m1 = Menu.objects.create(name="menu_test")

        MenuItem.objects.create(name="fanta", price=2.5, menu=self.m1)
        MenuItem.objects.create(name="cola", price=1.85, menu=self.m1)

        self.speyker = Place(name="speyker", menu=self.m1)
        self.speyker.save()


        self.t1 = Table(place=self.speyker)
        self.t1.save()

        self.t2 = Table(place=self.speyker)
        self.t2.save()

        self.t3 = Table(place=self.speyker)
        self.t3.save()

    def test_filter_contains_a(self):
        # find stuff that contains an 'a' ( 2 )
        a_tems = MenuItem.objects.filter(name__contains='a', menu=self.m1)
        self.assertEquals(len(a_tems), 2)

    def test_menu_item(self):
        # two items are created
        self.assertEquals(len(MenuItem.objects.filter(menu=self.m1)), 2)

    def test_find_cola(self):
        # find back cola
        cola = MenuItem.objects.get(name="cola", menu=self.m1)
        self.assertTrue(cola)

    def test_no_more_fristi(self):
        # do not find fristi
        fristi = MenuItem.objects.filter(name="fristi", menu=self.m1)
        self.assertFalse(fristi)

    def test_find_menu(self):
        # try to find all the menuitems for 1 menu
        menu = Menu.objects.get(name="menu_test")

        self.assertEquals(len(menu.menuitem_set.all()), 2)

    def test_find_a_menu_and_find_also_menuitems(self):
        """ Fetch a menu, and list the menu items  """

        # Menu
        menu = Menu(name="some menu")
        menu.save()


        # menuItems
        duvel = MenuItem(name="Duvel", price=3.8, menu=menu);
        duvel.save()

        vedet = MenuItem(name="Vedet", price=2.5, menu=menu)
        vedet.save()

        found_menu_list = Menu.objects.filter(name="some menu")
        self.assertEquals(len(found_menu_list.all()), 1)

        found_menu = found_menu_list[0]

        self.assertEquals(len(found_menu.menuitem_set.all()), 2 )

    def test_add_items_to_a_menu(self):
        # the setup-created menu
        m1 = Menu.objects.get(name="menu_test")

        self.assertEquals(m1.menuitem_set.get(name="fanta").price, Decimal('2.5'))
        self.assertEquals(m1.menuitem_set.get(name="cola").price, Decimal('1.85'))
        # start with 2 items
        self.assertEquals(len(m1.menuitem_set.all()), 2)

        # adding koffie
        MenuItem(name="koffie", price=1.8, menu=m1).save()

        found_menu = Menu.objects.get(pk=m1.pk)

        self.assertEquals(len(m1.menuitem_set.all()), 3)



    def test_menu_can_not_have_twice_the_same_item(self):

        # trying to add fanta twice
        self.assertRaises(MenuItem.objects.create, name="fanta", price=2.5, menu=self.m1)


    def test_getting_all_orders_for_speyker(self):
        Order.objects.create(table=self.t2)

        orders = self.speyker.get_orders()

        self.assertEquals(len(orders), 1)
        self.assertEquals(orders[0].table, self.t2)


    def test_place_order_get_ordered_items(self):
        order = place_order([('fanta', 2), ('cola', 1)], self.t2.pk)

        all_open_orders = services.get_open_orders(self.speyker)
        self.assertEquals(len(all_open_orders), 1)

        menuitems_amounts = all_open_orders[0].get_menuitems_amounts()


        for item, amount in menuitems_amounts:
            if item == "fanta":
                self.assertEquals(amount, 2)

            elif item == "cola":
                self.assertEquals(amount, 1)

            else:
                raise Exception("only cola and fanta!!")








