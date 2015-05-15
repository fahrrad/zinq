# Create your views here.
import json
import logging

from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from menus.models import MenuItem
from places.models import Table, Order
from places.views import logger
from django.conf import settings

logger = logging.getLogger(__name__)

# global variable that defines how to wait when refreshing an order
next_timeout = settings.NEXT_CHECKOUT_TIMEOUT


@csrf_exempt
def menu(request, table_uuid):
    """Typically called from a mobile device when scanning a qr code.
     The second parameter is the unique places identifier. This corresponds to a
     table, and uniquely identifies a menus.
    :param request:
    :param table_uuid:
    """
    table_uuid = table_uuid.lower()

    try:
        table = Table.objects.get(uuid=table_uuid)
        logger.debug("menus requested for table %s", table_uuid)
        place = table.place
        cat_menu_items = table.get_category_menu_items()
        logger.debug("returning %d menu items" % len(cat_menu_items))

    except Table.DoesNotExist as e:
        logger.error("Somebody tried to get a menu for a non " +
                     "existing table: %s", table_uuid)
        raise Http404()

    # render the template
    return render(request, "menus/order.html", {'cat_menu_items': cat_menu_items,
                                                'place': place,

                                                'table_uuid': table_uuid})


def menu_items(request, table_uuid):
    table_uuid = table_uuid.lower()
    # only for GET Requests
    if request.method == "GET":
        logger.debug("Got an GET for menu_items")

        try:
            table = Table.objects.get(pk=table_uuid)
            table_menu = table.get_menu()

            logger.info("getting menu items for menu id %d" % table_menu.id)
            return_str = serializers.serialize('json', MenuItem.objects.filter(menu=table_menu))

            return HttpResponse(return_str, content_type="text/json")
        except Table.DoesNotExist:
            logger.error("Table with uuid %s does not exists" % table_uuid)
            raise Http404
    else:
        return HttpResponse("No Get " + table_uuid)



@csrf_exempt
def place_order(request, table_uuid):
    """Accepts an order in the following form: [menu_item_id: amount:amount...]
    Returns 404 if table or one of the order-item ids are not found"""
    if request.method == 'POST':
        try:
            table = Table.objects.get(pk=table_uuid)
            o = Order.objects.create(table=table)
            for order_item, amount in request.POST.items():
                amount = int(amount)
                if amount > 0:
                    o.add_item_by_pk(order_item, amount)

        except Exception as e:
            o.delete()

            logger.warn(e)
            raise Http404()

        return HttpResponse(json.dumps({"order_uuid": o.pk}), content_type='application/json')
    else:
        return Http404()


def wait(request, order_uuid):
    """returns the view where the drinker is asked to wait."""
    return render(request, "menus/wait.html", {"order_uuid": order_uuid})


def wait_status(request, order_uuid):
    """
     This view returns a rendered view when HTTP_ACCEPT is not json, and a status
     code if json is requested.
    """
    response_data = dict()

    # lookup the orders in the database
    try:
        order = Order.objects.get(pk=order_uuid)
    except Order.DoesNotExist as e:
        logger.error("Somebody tried to fetch a non existing order! " + e)
        raise Http404()

    # Is the order done?
    response_data['status'] = order.status

    # how long should I wait for next check
    if order.status in (Order.DONE, Order.CANCELLED, Order.PAYED):
        response_data['next_check_timeout'] = 0
    else:
        response_data['next_check_timeout'] = next_timeout

    return_json = json.dumps(response_data)
    logger.debug(return_json)

    return HttpResponse(return_json, content_type="application/json")


def set_next_timeout(request, timeout):
    timeout = int(timeout)
    global next_timeout
    next_timeout = timeout
    return HttpResponse("Ok")