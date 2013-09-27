"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from decimal import Decimal

from django.test import TestCase, Client
from menu import services
from menu.models import MenuItem, Menu
from menu.services import place_order
from order.models import Order, OrderMenuItem
from place.models import Place, Table


class SimpleTest(TestCase):
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

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_create_an_order(self):
        cola = self.t1.get_menu().menuitem_set.get(name='cola')

        order = Order(table=self.t1)
        order.save()

        order.addItem(cola, 2)

        # When comparing with equals, the decimals are converted into floats
        # i guess.
        self.assertEqual(order.calculate_total_price(), Decimal('3.7'))

    def test_more_elaborate_order(self):

        order = Order(table=self.t1)
        order.save()

        order.addItem(self.m1.menuitem_set.get(name="cola"), 3)
        order.addItem(self.m1.menuitem_set.get(name="fanta"), 1)

        self.assertEqual(order.calculate_total_price(), Decimal('8.05'))
        self.assertEquals(len(order.menuItems.all()), 2)

        # get the menuitem count
        orderMenuItem = OrderMenuItem.objects.get(menuItem=self.m1.menuitem_set.get(name="cola"),
                                                  order=order)
        self.assertEquals(orderMenuItem.amount, 3)

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

    def test_place_order(self):
        all_open_orders = services.get_open_orders(self.speyker)

        # starting with no orders
        self.assertEquals(len(all_open_orders), 0)

        order = place_order([('fanta', 2), ('cola', 1)], self.t2.pk)

        all_open_orders = services.get_open_orders(self.speyker)
        self.assertEquals(len(all_open_orders), 1)

        self.assertEquals(len(all_open_orders[0].ordermenuitem_set.all()), 2)

    def test_place_order_price(self):

        order = place_order([('fanta', 2), ('cola', 1)], self.t1.pk)
        self.assertEqual(order.calculate_total_price(), Decimal('6.85'))

    def test_posting_an_order(self):
        table_pk = self.t1.pk

        c = Client()

        # Een colaatje astublief
        response = c.post("/menu/%s/" % table_pk, {'cola_amount': '3'})

        print response.status_code

        print response.content

        # find the order in the database
        orders = Order.objects.filter(table__pk=table_pk).all()
        self.assertEquals(len(orders), 1)

    def test_ordered_status(self):
        import json
        order = place_order([('fanta', 2), ('cola', 1)], self.t2.pk)

        c = Client()
        response = c.get("/wait/" + str(order.pk) + "/",
                         {}, False,
                         HTTP_ACCEPT="application/json",
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = json.loads(response.content)
        self.assertEquals(Order.ORDERED, response['status_code'])
        self.assertTrue(response['check_next'])

        order.status = Order.DONE
        order.save()

        # response should contain
        response = c.get("/wait/" + str(order.pk) + "/",
                         {}, False,
                         HTTP_ACCEPT="application/json",
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = json.loads(response.content)
        self.assertEquals(Order.DONE, response['status_code'])
        self.assertFalse(response['check_next'])
