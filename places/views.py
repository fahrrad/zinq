import logging
import string
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core import urlresolvers

from menus.services import place_order
from orders.models import Order
from places.models import Place, Table

from menus.models import MenuItem

logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "places/welcome.html")


def MENU(request, table_uuid):
    """ QR codes can be encoded more efficiently when they only contain capitals.
     To make it a bit easier on the eyes, I will make them lowercase here, and then
     call our normal menus function

     see http://code.google.com/p/zxing/wiki/BarcodeContents
    """
    url = urlresolvers.reverse("places.views.menus", args=(table_uuid.lower(),))
    return HttpResponseRedirect(url)


# needed because cannot use curl
@csrf_exempt
def menu(request, table_uuid):
    """Typically called from a mobile device when scanning a qr code.
     The second parameter is the unique places identifier. This corresponds to a
     table, and uniquely identifies a menus
    """
    if request.POST:
        # Got an order!!
        logger.info("orders!")
        logger.info("Post:" + repr(request.POST))

        # Loop over items in the orders, and ad them to a temp collection
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

        # places the orders
        order = place_order(item_name_amount, table_uuid)
        logger.info("saved an orders")

        # ok, orders is places, please wait now!
        return HttpResponseRedirect("/wait/" + str(order.pk))

    else:
        logger.debug("menus requested for table %s", table_uuid)
        try:
            table = Table.objects.get(uuid=table_uuid)
            place = table.place
            menu = table.get_menu()
        except :
            return render(request, "places/error.html", {'error_msg': "No table found with id %s!" % table_uuid})

        else:
            # render the template
            return render(request, "places/menu.html", {'menu': menu,
                                                       'places': place})


def landing(request):
    return render(request, 'landing.html')


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


def menu_items(request, table_uuid):
    # only for GET Requests
    if request.method == "GET":
        logger.debug("Got an GET for menu_items" )

        try:
            table = Table.objects.get(pk=table_uuid)
            menu = table.get_menu()

            logger.info("getting menutitems for menu id %d" % menu.id)
            return_str = serializers.serialize('json', MenuItem.objects.filter(menu=menu))

            return HttpResponse(return_str, content_type="text/json")
        except:
            logger.error("")
            raise Http404



    else:
        return HttpResponse("No Get " + table_uuid)


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


def qr_codes(request, place_id):
    """Renders a view containing a QR code for every table in the places!"""
    host_prefix = "HTTP://stormy-peak-3604.herokuapp.com/menu/"

    try:
        place = Place.objects.get(pk=int(place_id))

    except ObjectDoesNotExist as e:
        return render(request, "places/error.html",
                      {'error_msg': "No place found with id %s!" % place_id})
    table_qr_list = [host_prefix + x.pk + "/" for x in place.table_set.all()]

    return render(request, "places/qr_codes.html", {'table_qr_list': table_qr_list,
                                                    'place_name': place.name})
