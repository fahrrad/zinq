from menus.models import MenuItem
from orders.models import Order
from places.models import Table

__author__ = 'ward'


def get_open_orders(place):
    """
    Get a list of all the open (status = ordered) orders for one places.
    """
    tables = list(Table.objects.filter(place=place))
    return list(Order.objects.filter(table__in=tables,
                                     status=Order.ORDERED))


# Helper methods
def place_order(items, table_uuid):
    """
    Places an orders. The first argument is a list of pairs with menus names
    """
    table = Table.objects.get(uuid=table_uuid)
    order = Order.objects.create(table=table)

    for item_name, amount in items:
        menu_item = MenuItem.objects.get(menu=table.get_menu(), name=item_name)
        order.add_item_by_name(menu_item, amount)

    return order

