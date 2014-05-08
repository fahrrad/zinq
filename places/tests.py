"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import logging

from django.test import TestCase, Client
from models import Place, Table
from menus.models import Menu, MenuItem
from orders.models import Order

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

    def test_get_menu(self):
        c = Client()

        response = c.get('/orders/%s/' % self.dambert.pk,
                         HTTP_ACCEPT="application/json")

        logger.debug(response.content)
        self.assertEquals(json.loads(response.content)['interval'], 2000)

        table = self.dambert.table_set.get(table_nr=2)
        order = Order.objects.create(table=table)

        order.add_item_by_name(MenuItem.objects.get(name="duvel"), 2)
        order.add_item_by_name(MenuItem.objects.get(name="fanta"), 3)

        response = c.get('/orders/%s/' % self.dambert.pk,
                         HTTP_ACCEPT="application/json")

        logger.debug(response.content)

        json_object = json.loads(response.content)
        self.assertEquals(1, len(json_object['orders']))

        # one key, so we can fetch it
        key = json_object['orders'].keys()[0]
        self.assertEquals(key, order.pk)

        # tableNr
        self.assertEquals(json_object['orders'][key]['table_nr'], u'2')

        # table_nr + items
        self.assertEquals(len(json_object['orders'][key]), 2)

        # 2 items
        self.assertEquals(len(json_object['orders'][key]['item_amounts']), 2)

        # 2x duvel, 3x fanta
        for (item, amount) in json_object['orders'][key]['item_amounts']:
            if item == "duvel":
                self.assertEquals(amount, 2)
            if item == "fanta":
                self.assertEquals(amount, 3)

    def test_get_category_menu_items(self):
        cat_menu_items = self.t1.get_category_menu_items()

        self.assertEqual(2, len(cat_menu_items))
        self.assertIsNotNone(cat_menu_items['soft drink'])
        self.assertEqual(3, len(cat_menu_items['soft drink']))
