"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Place, Table
from menu.models import Menu, MenuItem


class SimpleTest(TestCase):
    def setUp(self):
        # place of all places
        self.dambert = Place.objects.create(name="dambert")

        self.dambert_menu = Menu.objects.create(name="default")
        self.dambert.menu = self.dambert_menu
        self.dambert.save()

        mi1 = MenuItem(name="cola", price=2.5, menu=self.dambert_menu)
        mi1.save()

        mi2 = MenuItem(name="cola light", price=2.8, menu=self.dambert_menu)
        mi2.save()

        mi3 = MenuItem(name="duvel", price=3.5, menu=self.dambert_menu)
        mi3.save()

        mi4 = MenuItem(name="fanta", price=1.5, menu=self.dambert_menu)
        mi4.save()


        # tables
        Table.objects.create(place=self.dambert)
        Table.objects.create(place=self.dambert)
        Table.objects.create(place=self.dambert)
        Table.objects.create(place=self.dambert)

    def test_finding_tables_for_dambert(self):

        dambert = Place.objects.get(name="dambert")
        self.assertEquals(len(dambert.table_set.all()), 4)

    def test_find_dambert_menu(self):

        place = Place.objects.get(name="dambert")
        t1_uuid = place.table_set.all()[1].uuid

        menu = Table.objects.get(uuid=t1_uuid).get_menu()

        # should have a menu!
        self.assertIsNotNone(menu)

        # menu should contain4 things
        self.assertEquals(len(menu.menuitem_set.all()), 4)

        # and fanta costs 1.5 here
        self.assertEquals(menu.menuitem_set.get(name="fanta").price, 1.5)

    def test_add_table(self):
        self.assertEquals(len(self.dambert.table_set.all()), 4)

        Table(place=self.dambert).save()

        self.assertEquals(len(self.dambert.table_set.all()), 5)








