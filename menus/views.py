# Create your views here.
import string
import logging

from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core import urlresolvers

from menus.models import MenuItem
from menus.services import place_order
from places.models import Table

logger = logging.getLogger(__name__)


def menu_items(request, table_uuid):
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


def MENU(request, table_uuid):
    """ QR codes can be encoded more efficiently when they only contain capitals.
     To make it a bit easier on the eyes, I will make them lowercase here, and then
     call our normal menus function

     see http://code.google.com/p/zxing/wiki/BarcodeContents
    """
    url = urlresolvers.reverse("places.views.menus", args=(table_uuid.lower(),))
    return HttpResponseRedirect(url)


# When testing using Curl, need exempt
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
            table_menu = table.get_menu()
        except Table.DoesNotExist:
            return render(request, "places/error.html", {'error_msg': "No table found with id %s!" % table_uuid})

        else:
            # render the template
            return render(request, "places/menu.html", {'menu': table_menu,
                                                        'places': place})