# Create your views here.
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from orders.models import Order
from places.models import Place, Table
from places.views import logger

import logging

logging.basicConfig()
#
# credentials = pika.PlainCredentials('guest', 'guest')
# conn_properties = pika.ConnectionParameters('localhost') #, 5672, '/', credentials)
# connection = pika.BlockingConnection(conn_properties)
# channel = connection.channel()
# channel.queue_declare(queue='hello')


def wait_status(request, order_uuid):
    """
     This view returns a rendered view when HTTP_ACCEPT is not json, and a status
     code if json is requested.
    """
    response_data = dict()

    # lookup the orders in the database
    order = Order.objects.get(pk=order_uuid)

    response_data['status_done'] = order.status == Order.DONE

    # how long should I wait for next check
    response_data['next_check_timeout'] = 2000

    return_json = json.dumps(response_data)
    logger.debug(return_json)

    return HttpResponse(return_json, content_type="application/json")


def wait(request, order_uuid):
    """returns the view where the drinker is asked to wait."""
    return render(request, "orders/wait.html", {"order_uuid": order_uuid})


def orders(request, place_pk):
    """list all the orders for a given places
        Results in something like this:

        |-------------------------------------------
        | interval  = 2000
        | orders: |---------------------------------
        |         | pk : |--------------------------
        |         |      | tableNr
        |         |      | item_amounts:|-----------
        |         |      |              | (name, amount)
        |         |      |              | (name, amount)
        |         |      |              |-----------
        |         |      |--------------------------
        |         |
        |         |
        |         | pk : |--------------------------
        |         |      | tableNr
        |         |      | item_amounts:|-----------
        |         |      |              | (name, amount)
        |         |      |              | (name, amount)
        |         |      |              |-----------
        |         |      |--------------------------
        |         |---------------------------------
        |-------------------------------------------
    """

    # try get places
    try:
        place = Place.objects.get(pk=place_pk)
        place_orders = place.get_orders()

    except ObjectDoesNotExist:
        return render(request, "places/error.html", {'error_msg': "No places found with id %s!" % place_pk})

            # check if the request is coming from an ajax call (The refresh code on the page)
    if 'application/json' in request.META['HTTP_ACCEPT'].split(','):
        return_values = dict()
        # interval to wait for next request
        return_values['interval'] = 2000
        return_values['orders'] = dict()

        for order in place_orders:
            return_values['orders'][order.pk] = dict()
            return_values['orders'][order.pk]['table_nr'] = order.table.table_nr
            return_values['orders'][order.pk]['item_amounts'] = order.get_menuitems_amounts()

        # just return the data
        return HttpResponse(json.dumps(return_values), content_type='application/json')
    else:
        return render(request, "places/orders.html", {'orders': place_orders})


def place_order(request, table_uuid):
    """Accepts an order in the following form: [{ pk:menu_item_id, amount:amount ... }]"""

    if request.method == 'GET' and 'order' in request.GET.keys():
        order = request.POST['order']
        try:
            table = Table.objects.get(pk=table_uuid)
            o = Order(table=table)
            for order_item in order:
                o.add_item_by_pk(order_item.pk, order_item.amount)
        except:
            raise Http404()

        return HttpResponse(json.dumps({"order_id": o.pk}), content_type='text/json')


def rm_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.DONE
        order.save()

    except Exception as e:
        logger.error(e)
        return render(request, "places/error.html", {"error_msg": e})

    logger.info('Order id %s is deleted' % order_id)

    return HttpResponse("Order %s deleted" % order_id)


def get_order_app(request, table_uuid):
    return render(request, 'orders/order_app.html', {"table_uuid":table_uuid})


def sent_message(request):
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')