# Create your views here.
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from places.models import Place, Table


import logging

logging.basicConfig()
#
# credentials = pika.PlainCredentials('guest', 'guest')
# conn_properties = pika.ConnectionParameters('localhost') #, 5672, '/', credentials)
# connection = pika.BlockingConnection(conn_properties)
# channel = connection.channel()
# channel.queue_declare(queue='hello')

logger = logging.getLogger(__name__)

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
    response_data['status_done'] = order.status == Order.DONE

    # how long should I wait for next check
    response_data['next_check_timeout'] = 2000

    return_json = json.dumps(response_data)
    logger.debug(return_json)

    return HttpResponse(return_json, content_type="application/json")


def wait(request, order_uuid):
    """returns the view where the drinker is asked to wait."""
    return render(request, "orders/wait.html", {"order_uuid": order_uuid})


def orders_open(request, place_pk):
    """ Returns json object with the orders for this place.
    Results looks like this:

    |---LIST------------------------------------
    | |---MAP---------------------
    | | pk
    | | table_nr
    | | seconds
    | | total
    | | item_amounts:|-----------
    | |              | (name, amount, price)
    | |              | (name, amount, price)
    | |              |-----------
    | |--------------------------
    |
    | |---MAP--------------------
    | | pk
    | | table_nr
    | | seconds
    | | total
    | | item_amounts:|-----------
    | |              | (name, amount, price)
    | |              | (name, amount, price)
    | |              |-----------
    | |--------------------------
    |-------------------------------------------
    """
    try:
        place = Place.objects.get(pk=place_pk)
        place_orders = place.get_orders()

    except Place.DoesNotExist as e:
        logger.error("Someone tried to fetch orders for a place (pk %s) that does not exists. Request %s"
                     % (place_pk, request))
        raise Http404()

    # check if the request is coming from an ajax call (The refresh code on the page)
    if 'application/json' in request.META['HTTP_ACCEPT'].split(','):
        # interval to wait for next request
        orders = list()
        for order in place_orders:
            return_order = dict()
            return_order['pk'] = order.pk
            return_order['table_nr'] = order.table.table_nr
            return_order['seconds'] = 1
            return_order["total"] = 25.5
            return_order['item_amounts'] = order.get_menuitems_amounts()

            orders.append(return_order)


        # just return the data
        return HttpResponse(json.dumps(orders), content_type='application/json')
    else:
        logger.error("got a request without HTTP_ACCEPT = application/json")
        raise Http404()


def orders(request, place_pk):
    return render(request, "places/orders.html", {'place_pk': place_pk})


@csrf_exempt
def place_order(request, table_uuid):
    """Accepts an order in the following form: [{ pk:menu_item_id, amount:amount ... }]
    Returns 404 if table or one of the order-item ids are not found"""
    if request.method == 'POST':
        try:
            table = Table.objects.get(pk=table_uuid)
            o = Order.objects.create(table=table)
            for order_item, amount in request.POST.items():
                o.add_item_by_pk(order_item, amount)
        except Exception as e:
            logger.warn(e)
            raise Http404()

        return HttpResponse(json.dumps({"order_uuid": o.pk}), content_type='application/json')
    else:
        return Http404()


def order_done(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.DONE
        order.save()

    except Order.DoesNotExist as e:
        logger.error("trying to put an unexisting order on done! request: %s " % request)
        # raise Http404()

    logger.info('Order id %s is done' % order_id)

    return HttpResponse("Order %s set to done" % order_id)