import json
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import serializers

from places.models import Place, Order, Table




# Logging
logger = logging.getLogger(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)


channel = None


def landing(request):
    table = Table.objects.filter(place__pk=1).first()
    return render(request, 'landing.html', {'table_uuid': table.pk})


def qr_codes(request, place_id):
    """Renders a view containing a QR code for every table in the places!"""
    host_prefix = settings.MENU_URL
    # host_prefix = "http://192.168.0.178:8000/menu/"
    try:
        place = Place.objects.get(pk=int(place_id))
    except place.DoesNotExist:
        return render(request, "places/error.html",
                      {'error_msg': "No place found with id %s!" % place_id})
    table_qr_list = [host_prefix + x.pk.upper() + "/" for x in place.table_set.all()]
    place_orders = str.format("{}ORDERS/{}", settings.HOST_URL, place_id)

    return render(request, "places/qr_codes.html", {'table_qr_list': table_qr_list,
                                                    'place_name': place.name,
                                                    'place_orders': place_orders})




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
    response_data['next_check_timeout'] = 2000

    return_json = json.dumps(response_data)
    logger.debug(return_json)

    return HttpResponse(return_json, content_type="application/json")


def wait(request, order_uuid):
    """returns the view where the drinker is asked to wait."""
    return render(request, "menus/wait.html", {"order_uuid": order_uuid})


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
        logger.error("Someone tried to fetch orders for a place (pk %s) that does not exists. Request %s, Error %s"
                     , place_pk, request, e.message)
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

            # log only to channel when available
            channel and channel.basic_publish(exchange="",
                                              routing_key="order",
                                              body=serializers.serialize("json", o.ordermenuitem_set.all()))
        except Exception as e:
            o.delete()

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
        logger.error("trying to put an non existing order on done! request: %s " % request)
        # raise Http404()
        return Http404()
    logger.info('Order id %s is done' % order_id)

    return HttpResponse("Order %s set to done" % order_id)


def order_in_progress(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.IN_PROGRESS
        order.save()
    except Order.DoesNotExist as e:
        logger.error("trying to change state of an order that does not exists to in progress %s" % request)
        return Http404()

    return HttpResponse("")


def order_cancel(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.CANCELLED
        order.save()

    except Order.DoesNotExist as e:
        logger.error("trying to cancel an non existing order! request: %s " % request)
        # raise Http404()

    logger.info('Order id %s is cancelled' % order_id)

    return HttpResponse("Order %s was cancelled" % order_id)
