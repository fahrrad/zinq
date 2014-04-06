"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import logging
from decimal import Decimal
from django.db import IntegrityError, transaction

from django.test import TestCase
from menus import services
from menus.models import MenuItem, Menu, Category
from menus.services import place_order
from orders.models import Order
from places.models import Place, Table

# integration testing
from django.test.client import Client

logger = logging.getLogger(__name__)

import contextlib

class MenuTest(TestCase):
    """ Simple tests on the MenuItem object, and there menus group """

    def setUp(self):
        """create some stuff"""
        self.m1 = Menu.objects.create(name="menu_test")

        self.mi_fanta = MenuItem.objects.create(name="fanta", price=2.5, menu=self.m1)
        self.mi_cola = MenuItem.objects.create(name="cola", price=1.85, menu=self.m1)

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
        a_items = MenuItem.objects.filter(name__contains='a', menu=self.m1)
        self.assertEquals(len(a_items), 2)

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
        # try to find all the menu items for 1 menus
        menu = Menu.objects.get(name="menu_test")

        self.assertEquals(len(menu.menuitem_set.all()), 2)

    def test_find_a_menu_and_find_also_menu_items(self):
        """ Fetch a menus, and list the menus items  """

        # Menu
        menu = Menu(name="some menus")
        menu.save()

        # menuItems
        duvel = MenuItem(name="Duvel", price=3.8, menu=menu)
        duvel.save()

        vedet = MenuItem(name="Vedet", price=2.5, menu=menu)
        vedet.save()

        found_menu_list = Menu.objects.filter(name="some menus")
        self.assertEquals(len(found_menu_list.all()), 1)

        found_menu = found_menu_list[0]

        self.assertEquals(len(found_menu.menuitem_set.all()), 2)

    def test_add_items_to_a_menu(self):
        # the setup-created menus
        m1 = Menu.objects.get(name="menu_test")

        self.assertEquals(m1.menuitem_set.get(name="fanta").price, Decimal('2.5'))
        self.assertEquals(m1.menuitem_set.get(name="cola").price, Decimal('1.85'))

        # start with 2 items
        self.assertEquals(len(m1.menuitem_set.all()), 2)

        # adding coffee
        MenuItem(name="koffie", price=1.8, menu=m1).save()

        found_menu = Menu.objects.get(pk=m1.pk)

        self.assertEquals(len(found_menu.menuitem_set.all()), 3)

    def test_menu_can_not_have_twice_the_same_item(self):

        # trying to add fanta twice
        self.assertRaises(MenuItem.objects.create, name="fanta", price=2.5, menu=self.m1)

    def test_getting_all_orders_for_speyker(self):
        Order.objects.create(table=self.t2)

        orders = self.speyker.get_orders()

        self.assertEquals(len(orders), 1)
        self.assertEquals(orders[0].table, self.t2)

    def test_place_order_get_ordered_items(self):
        place_order([('fanta', 2), ('cola', 1)], self.t2.pk)

        all_open_orders = services.get_open_orders(self.speyker)
        self.assertEquals(len(all_open_orders), 1)

        menu_items_amounts = all_open_orders[0].get_menuitems_amounts()
        for item, amount in menu_items_amounts:
            if item == "fanta":
                self.assertEquals(amount, 2)

            elif item == "cola":
                self.assertEquals(amount, 1)

            else:
                raise Exception("only cola and fanta!!")

    def test_get_menu_items(self):
        """Testing the json response for menu items that"""
        # pks can not be stored, because in postgres the sequences are preserved in between tests
        json_menu_items = [{u'pk': self.mi_cola.pk, u'model': u'menus.menuitem',
                            u'fields': {u'menu': self.m1.pk, u'price': u'1.85', u'name': u'cola'}},
                           {u'pk': self.mi_fanta.pk, u'model': u'menus.menuitem',
                            u'fields': {u'menu': self.m1.pk, u'price': u'2.50', u'name': u'fanta'}}]

        c = Client()
        r = c.get('/mi/'+self.t1.pk, follow=True)

        self.assertEqual(200, r.status_code)
        self.assertJSONEqual(r.content, json_menu_items)

    def test_add_items_to_order_by_id(self):
        """Testing that adding menu items by id has the correct effect on the price"""
        o = Order(table=self.t1)
        o.save()

        mi = self.m1.menuitem_set.all()[0]
        o.add_item_by_pk(mi.pk, 2)

        expected_price = mi.price * 2
        self.assertAlmostEqual(o.calculate_total_price(), expected_price)
        self.assertEqual(1, o.menuItems.count())

        mi2 = self.m1.menuitem_set.all()[0]
        o.add_item_by_pk(mi2.pk, 3)

        expected_price = mi.price * 2 + mi2.price * 3
        self.assertAlmostEqual(o.calculate_total_price(), expected_price)
        self.assertEqual(2, o.menuItems.count())

    def test_create_category(self):
        c = Category(name='beer', place=self.speyker)
        c.save()

        found_c = Category.objects.filter(place=self.speyker)
        self.assertEqual(found_c.count(), 1)

        found_c = found_c.all()[0]

        self.assertEqual(found_c.name, 'beer')

    def test_category_has_to_be_unique(self):
        self.assertEqual(Category.objects.all().count(), 0)

        Category.objects.create(name='beer', place=self.speyker)

        # Cannot add a second beer to this place
        #
        # the atomic() is needed because of the error we expect. If I did not do this,
        # later questions to this transaction would result in
        # "An error occurred in the current transaction. You can't execute queries until
        # the end of the 'atomic' block."
        # see https://docs.djangoproject.com/en/1.6/topics/db/transactions/#django.db.transaction.atomic
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name='beer', place=self.speyker)

        # But another Category is no problem
        Category.objects.create(name='ham&cheese', place=self.speyker)

        # Also, Beer can be added to another place!
        p2 = Place.objects.create(name="bogus place")
        Category.objects.create(name='beer', place=p2)