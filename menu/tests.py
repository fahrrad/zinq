"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from menu.models import MenuItem, Menu
from uuid import uuid4

class MenuTest(TestCase):
    """ Simple tests on the MenuItem object, and there menu group """

    def setUp(self):
        """create some stuff"""
        m1 = Menu.objects.create(name="menu1")

        MenuItem.objects.create(name="fanta", price=2.5, menu=m1)
        MenuItem.objects.create(name="cola", price=1.85, menu=m1)


    def test_filter_contains_a(self):
        # find stuff that contains an 'a' ( 2 )
        a_tems = MenuItem.objects.filter(name__contains='a')
        self.assertEquals(len(a_tems), 2)
       

    def test_menu_item(self):
        # two items are created
        self.assertEquals(len(MenuItem.objects.all()), 2)


    def test_find_cola(self):
        # find back cola
        cola = MenuItem.objects.get(name="cola")
        self.assertTrue(cola)


    def test_no_more_fristi(self):
        # do not find fristi
        fristi = MenuItem.objects.filter(name="fristi")
        self.assertFalse(fristi)

    def test_find_menu(self):
        # try to find all the menuitems for 1 menu
        menu = Menu.objects.get(name="menu1")

        self.assertEquals(len(menu.menuitem_set.all()), 2)

    def test_find_a_menu_and_find_also_menuitems(self):
        """ Fetch a menu, and list the menu items  """

        # Menu
        menu = Menu(name="some menu")
        menu.save()


        # menuItems
        duvel = MenuItem(name="Duvel", price=3.8, menu=menu)
        duvel.save()

        vedet = MenuItem(name="Vedet", price=2.5, menu=menu)
        vedet.save()

        found_menu_list = Menu.objects.filter(name="some menu")
        self.assertEquals(len(found_menu_list.all()), 1)

        found_menu = found_menu_list[0]

        self.assertEquals(len(found_menu.menuitem_set.all()), 2 )


    def test_add_items_to_a_menu(self):
        # the setup-created menu
        m1 = Menu.objects.get(pk=1)

        self.assertEquals(m1.menuitem_set.get(name="fanta").price, 2.5 )
        self.assertEquals(m1.menuitem_set.get(name="cola").price, 1.85 )
        # start with 2 items
        self.assertEquals(len(m1.menuitem_set.all()), 2)

        # adding koffie
        MenuItem(name="koffie", price=1.8, menu=m1).save()

        found_menu = Menu.objects.get(pk=1)

        self.assertEquals(len(m1.menuitem_set.all()), 3)







