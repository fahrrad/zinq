from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from menu.services import place_order
from place.models import Place, Table
from menu.models import Menu, MenuItem, Order, OrderMenuItem
import logging
import string
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "place/welcome.html")


# needed because
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

        return HttpResponseRedirect("/menu/" + table_uuid)

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
        Order.objects.get(pk=order_id).delete()
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




