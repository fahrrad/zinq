from django.shortcuts import render
from django.http import HttpResponseRedirect
from menu.services import place_order
from place.models import Place, Table
from menu.models import Menu, MenuItem, Order, OrderMenuItem
import logging
import string

logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "place/welcome.html")


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
            if str(key).__contains__("_amount") and int(amount) > 0:
                item_name = string.replace(key, "_amount", "")
                logger.info("key " + item_name)
                logger.info("amount " + amount)
                item_name_amount.append((item_name, amount))

        # place the order
        order = place_order(item_name_amount, table_uuid)

        return HttpResponseRedirect("/menu/" + table_uuid)

    else:
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





