"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from menu import services
from menu.models import MenuItem, Menu, Order, OrderMenuItem
from menu.services import place_order
from place.models import Place, Table
from decimal import Decimal

# integration testing
from django.test.client import Client


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

        found_menu = Menu.objects.get(pk=1)

        self.assertEquals(len(m1.menuitem_set.all()), 3)

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

    def test_menu_can_not_have_twice_the_same_item(self):

        # trying to add fanta twice
        self.assertRaises(MenuItem.objects.create, name="fanta", price=2.5, menu=self.m1)

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
        table_pk = 'f64f609e75bd4afbbc18cf7f29fcafde'

        c = Client()

        # Een colaatje astublief
        response = c.post("/menu/%s/" % table_pk, {'cola_amount': '3'})

        print response.status_code

        print response.content

        # find the order in the database
        orders = Order.objects.filter(table__pk=table_pk).all()
        self.assertEquals(len(orders), 1)

    def test_getting_all_orders_for_speyker(self):
        Order.objects.create(table=self.t2)

        orders = self.speyker.get_orders()

        self.assertEquals(len(orders), 1)
        self.assertEquals(orders[0].table, self.t2)


    def test_place_order_get_ordered_items(self):
        order = place_order([('fanta', 2), ('cola', 1)], self.t2.pk)

        all_open_orders = services.get_open_orders(self.speyker)
        self.assertEquals(len(all_open_orders), 1)

        menuitems_amounts = all_open_orders[0].get_menuitems_amounts();


        for item, amount in menuitems_amounts:
            if item == "fanta":
                self.assertEquals(amount, 2)

            elif item == "cola":
                self.assertEquals(amount, 1)

            else:
                raise Exception("only cola and fanta!!")









