from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from menu.services import place_order
from place.models import Place, Table
from menu.models import Menu, MenuItem, Order, OrderMenuItem
import logging
import string
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "place/welcome.html")


# needed because cannot use curl
@csrf_exempt
def menu(request, table_uuid):
    """Typically called from a mobile device when scanning a qr code.
     The second parameter is the unique place identifier. This corresponds to a
     table, and uniquely identifies a menu
    """

    if request.POST:
        # Got an order!!
        logger.info("order!")
        logger.info("Post:" + repr(request.POST))

        # Loop over items in the order, and ad them to a temp collection
        item_name_amount = []
        for key, amount in request.POST.items():

            # only keys that end in _amount should have a numeric value
            if string.find(key, "_amount") > -1:
                amount = int(amount)
                if amount > 0:
                    item_name = string.replace(key, "_amount", "")

                    logger.info("key " + item_name)
                    logger.info("amount %d" % amount)

                    item_name_amount.append((item_name, amount))

        # place the order
        order = place_order(item_name_amount, table_uuid)
        logger.info("saved an order")

        # ok, order is place, please wait now!
        return HttpResponseRedirect("/wait/" + str(order.pk))

    else:
        logger.info("menu requested for table %s", table_uuid)
        try:
            table = Table.objects.get(uuid=table_uuid)
            place = table.place
            menu = table.get_menu()
        except:
            return render(request, "place/error.html", {'error_msg': "No table found with id %s!" % table_uuid})

        return render(request, "place/menu.html", {'menu': menu,
                                                   'place': place})


def landing(request):
    return render(request, 'landing.html')


def rm_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.status = Order.DONE
        order.save()

    except Exception as e:
        logger.error(e)
        return render(request, "place/error.html", {"error_msg" : e})

    logger.info('Order id %s is deleted' % order_id)

    return HttpResponse("Order %s deleted" % order_id)

def orders(request, place_pk):
    """list all the orders for a given place"""

    # try get place
    try:
        place = Place.objects.get(pk=place_pk)
    except:
        return render(request, "place/error.html", {'error_msg': "No place found with id %s!" % place_pk})

    orders = place.get_orders()

    return render(request, "place/orders.html", {'orders': orders})


def wait(request, order_uuid):
    logger.debug("request type " + str(request.encoding))
    logger.debug("is ajax: " + str(request.is_ajax()))
    logger.debug("request.META.CONTENT_TYPE " + str(request.META["HTTP_ACCEPT"]))

    if request.META["HTTP_ACCEPT"].split(',')[0] == "application/json":
        response_data = dict()

        # lookup the order in the database
        order = Order.objects.get(pk=order_uuid)
        status_display = order.get_status_display()
        status_code = order.status

        response_data['status_display'] = status_display

        # should I check again
        check_next = status_code != Order.DONE

        # how long should I wait for next check
        next_check_timeout = 2000

        response_data['next_check_timeout'] = next_check_timeout
        response_data['check_next'] = check_next

        return_json = json.dumps(response_data)
        logger.debug(return_json)

        return HttpResponse(return_json, content_type="application/json")



    return render(request, "place/waiting.html")


