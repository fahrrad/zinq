# Create your views here.
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from orders.models import Order
from places.models import Place, Table
from places.views import logger


def wait(request, order_uuid):
    """returns the view where the drinker is asked to wait.
     This view returns a rendered view when HTTP_ACCEPT is not json, and a status
     code if json is requested.
    """
    if request.META["HTTP_ACCEPT"].split(',')[0] == "application/json":
        response_data = dict()

        # lookup the orders in the database
        order = Order.objects.get(pk=order_uuid)
        status_display = order.get_status_display()
        status_code = order.status

        response_data['status_display'] = status_display
        response_data['status_code'] = status_code

        # should I check again
        check_next = status_code != Order.DONE

        # how long should I wait for next check
        next_check_timeout = 2000

        response_data['next_check_timeout'] = next_check_timeout
        response_data['check_next'] = check_next

        return_json = json.dumps(response_data)
        logger.debug(return_json)

        return HttpResponse(return_json, content_type="application/json")

    return render(request, "places/waiting.html")


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
        orders = place.get_orders()

    except ObjectDoesNotExist:
        return render(request, "places/error.html", {'error_msg': "No places found with id %s!" % place_pk})

            # check if the request is coming from an ajax call (The refresh code on the page)
    if 'application/json' in request.META['HTTP_ACCEPT'].split(','):
        return_values = dict()
        # interval to wait for next request
        return_values['interval'] = 2000
        return_values['orders'] = dict()

        for order in orders:
            return_values['orders'][order.pk] = dict()
            return_values['orders'][order.pk]['table_nr'] = order.table.table_nr
            return_values['orders'][order.pk]['item_amounts'] = order.get_menuitems_amounts()

        # just return the data
        return HttpResponse(json.dumps(return_values), content_type='application/json')
    else:
        return render(request, "places/orders.html", {'orders': orders})


def place_order(request, table_uuid):
    """Accepts an order in the following form: [{ pk:menu_item_id, amount:amount ... }]"""

    if request.method == 'POST' and 'order' in request.POST.keys():
        order = request.POST['order']

        try:
            table = Table.objects.get(pk=order.table)
            o = Order(table=table)
            for order_item in order:
                o.add_item_by_pk(order_item.pk, order_item.amount)
        except:
            raise Http404()


def rm_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.DONE
        order.save()

    except Exception as e:
        logger.error(e)
        return render(request, "places/error.html", {"error_msg" : e})

    logger.info('Order id %s is deleted' % order_id)

    return HttpResponse("Order %s deleted" % order_id)