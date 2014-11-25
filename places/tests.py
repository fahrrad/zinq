"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from decimal import Decimal
import json
import logging

from django.test import TestCase, Client

from models import Place, Table, Order, OrderMenuItem
from menus.models import Menu, MenuItem


logger = logging.getLogger(__name__)


class SimpleTest(TestCase):
    def setUp(self):
        # places of all places
        self.dambert = Place.objects.create(name="dambert")

        self.dambert_menu = Menu.objects.create(name="default")
        self.dambert.menu = self.dambert_menu
        self.dambert.save()

        self.mi1 = MenuItem.objects.create(name="cola",
                                           price=2.5,
                                           menu=self.dambert_menu,
                                           category="soft drink")

        self.mi2 = MenuItem.objects.create(name="cola light",
                                           price=2.8,
                                           menu=self.dambert_menu,
                                           category="soft drink")

        self.mi3 = MenuItem.objects.create(name="duvel",
                                           price=3.5,
                                           menu=self.dambert_menu,
                                           category="beer")

        self.mi4 = MenuItem.objects.create(name="fanta",
                                           price=1.5,
                                           menu=self.dambert_menu,
                                           category="soft drink")

        # tables
        self.t1 = Table.objects.create(place=self.dambert, table_nr=1)
        self.t2 = Table.objects.create(place=self.dambert, table_nr=2)
        self.t3 = Table.objects.create(place=self.dambert, table_nr=3)
        self.t4 = Table.objects.create(place=self.dambert, table_nr=4)

    def test_finding_tables_for_dambert(self):
        dambert = Place.objects.get(name="dambert")
        self.assertEquals(len(dambert.table_set.all()), 4)

    def test_find_dambert_menu(self):
        place = Place.objects.get(name="dambert")
        t1_uuid = place.table_set.all()[1].uuid

        menu = Table.objects.get(uuid=t1_uuid).get_menu()

        # should have a menus!
        self.assertIsNotNone(menu)

        # menus should contain4 things
        self.assertEquals(len(menu.menuitem_set.all()), 4)

        # and fanta costs 1.5 here
        self.assertEquals(menu.menuitem_set.get(name="fanta").price, 1.5)

    def test_add_table(self):
        self.assertEquals(len(self.dambert.table_set.all()), 4)

        Table(place=self.dambert).save()

        self.assertEquals(len(self.dambert.table_set.all()), 5)

    def test_1to1_menu_place(self):
        self.assertRaises(Place.objects.create,
                          name="some places that copies a menus",
                          menu=self.dambert_menu)

    def test_get_category_menu_items(self):
        cat_menu_items = self.t1.get_category_menu_items()

        self.assertEqual(2, len(cat_menu_items))
        self.assertIsNotNone(cat_menu_items['soft drink'])
        self.assertEqual(3, len(cat_menu_items['soft drink']))



class SimpleTest_orders(TestCase):
    def setUp(self):
        """create some stuff"""
        self.m1 = Menu.objects.create(name="menu_test")

        self.mi1 = MenuItem.objects.create(name="fanta", price=2.5, menu=self.m1)
        self.mi2 = MenuItem.objects.create(name="cola", price=1.85, menu=self.m1)

        self.speyker = Place(name="speyker", menu=self.m1)
        self.speyker.save()

        self.t1 = Table(place=self.speyker)
        self.t1.save()

        self.t2 = Table(place=self.speyker, table_nr="2")
        self.t2.save()

        self.t3 = Table(place=self.speyker)
        self.t3.save()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_create_an_order(self):
        cola = self.t1.get_menu().menuitem_set.get(name='cola')

        order = Order(table=self.t1)
        order.save()

        order.add_menuitem(cola, 2)

        # When comparing with equals, the decimals are converted into floats
        # i guess.
        self.assertEqual(order.calculate_total_price(), Decimal('3.7'))

    def test_more_elaborate_order(self):
        order = Order(table=self.t1)
        order.save()

        order.add_menuitem(self.m1.menuitem_set.get(name="cola"), 3)
        order.add_menuitem(self.m1.menuitem_set.get(name="fanta"), 1)

        self.assertEqual(order.calculate_total_price(), Decimal('8.05'))
        self.assertEquals(len(order.menuItems.all()), 2)

        # get the menu item count
        order_menu_item = OrderMenuItem.objects.get(menuItem=self.m1.menuitem_set.get(name="cola"),
                                                    order=order)
        self.assertEquals(order_menu_item.amount, 3)

    def test_order_statuses(self):
        order = Order(table=self.t1)

        # fist status is ordered ( default )
        self.assertEquals(order.get_status_display(), 'Ordered')

        order.proceed()
        # second status is done
        self.assertEquals(order.get_status_display(), 'Done')

        order.proceed()
        # last status is payed
        self.assertEquals(order.get_status_display(), 'Payed')

        # no next step, except an exception
        self.assertRaises(order.proceed)

    def test_place_order_price(self):
        order = {self.mi1.pk: 2, self.mi2.pk: 1}
        c = Client()
        c.post("/order/p/" + self.t1.pk + '/', order)

        o = Order.objects.get(table=self.t1)
        self.assertEqual(o.calculate_total_price(), Decimal('6.85'))

    def test_posting_an_order(self):
        table_pk = self.t1.pk
        c = Client()

        # a cola please
        response = c.post("/order/p/%s/" % table_pk, {'cola_amount': '3'})

        print response.status_code

        print response.content

        # find the orders in the database
        orders = Order.objects.filter(table__pk=table_pk).all()
        self.assertEquals(len(orders), 1)

    def test_ordered_status(self):
        import json

        order = Order.objects.create(table=self.t2)
        order.add_menuitem(self.mi1, 2)
        order.add_menuitem(self.mi2, 1)
        order.save()

        c = Client()
        response = c.get("/wait_status/" + str(order.pk) + "/", {}, False,
                         HTTP_ACCEPT="application/json",
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = json.loads(response.content)
        self.assertEquals(Order.ORDERED, response['status_done'])
        self.assertTrue(response.get('next_check_timeout'))

        order.status = Order.DONE
        order.save()

        # response should contain
        response = c.get("/wait_status/" + str(order.pk) + "/", {}, False,
                         HTTP_ACCEPT="application/json",
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = json.loads(response.content)
        self.assertEquals(Order.DONE, response['status_done'])

    def test_place_order_rest_call(self):
        self.assertEqual(Order.objects.filter(table=self.t1).count(), 0)

        c = Client()

        post_order = {self.mi1.pk: 2, self.mi2.pk: 6}

        r = c.post('/order/p/%s/' % self.t1.pk, post_order, follow=True)
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Order.objects.filter(table=self.t1).count(), 1)

    def test_orders_open(self):
        order = Order.objects.create(table=self.t2)
        order.add_menuitem(self.mi1, 2)
        order.add_menuitem(self.mi2, 1)
        order.save()

        c = Client()
        r = c.get('/order/o/%d/' % self.speyker.pk, {}, False,
                  HTTP_ACCEPT="application/json",
                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        orders = json.loads(r.content)

        self.assertEqual(len(orders), 1)
        order = orders[0]
        self.assertEquals(len(order), 5)
        self.assertEquals(order['table_nr'], self.t2.table_nr)
        self.assertIsNotNone(order['pk'])
        self.assertEquals(order['seconds'], 1)

        item_amounts_ = order['item_amounts']
        self.assertEquals(len(item_amounts_), 2)

        item_amounts_1 = item_amounts_[0]
        self.assertEquals(item_amounts_1[0], 'fanta')
        self.assertEquals(item_amounts_1[1], 2)
        self.assertEquals(item_amounts_1[2], '5')
