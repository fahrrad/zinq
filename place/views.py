from django.shortcuts import render
from django.http import HttpResponseRedirect
from place.models import Place, Table
from menu.models import Menu, MenuItem
import logging

logger = logging.getLogger(__name__)

def welcome(request):
    return render(request, "place/welcome.html")

def menu(request, table_uuid):
    """Typicaly called from a mobile device when scanning a qr code.
     The second parameter is the unique place identifier. This corresponds to a
     table, and uniquely identies a menu
    """

    if request.POST:
        # Got an order!!
        logger.info("order!")
        logger.info("Post:" + repr(request.POST))



        return HttpResponseRedirect("/menu/" + table_uuid)
    else:
        try:
            table = Table.objects.get(uuid=table_uuid)
            place = table.place
            menu = table.get_menu()
        except:
            return render(request, "place/error.html", {'error_msg' : "No table found with id %s!" % table_uuid})


        return  render(request, "place/menu.html", {'menu': menu,
                                                'place': place})

def landing(request):
    return render(request, 'landing.html')
