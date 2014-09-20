# Create your views here.
import logging

from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pika

from menus.models import MenuItem
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


# When testing using Curl, need exempt
@csrf_exempt
def menu(request, table_uuid):
    """Typically called from a mobile device when scanning a qr code.
     The second parameter is the unique places identifier. This corresponds to a
     table, and uniquely identifies a menus.
    :param request:
    :param table_uuid:
    """
    channel = None

    try:
        table = Table.objects.get(uuid=table_uuid)
        logger.debug("menus requested for table %s", table_uuid)
        place = table.place
        cat_menu_items = table.get_category_menu_items()
        logger.debug("returning %d menu items" % len(cat_menu_items))

        msg_properties = pika.BasicProperties()
        msg_properties.content_type = "text/plain"

        if channel:
            channel.basic_publish(body=table_uuid,
                                  exchange="menu_exchange",
                                  properties=msg_properties,
                                  routing_key="logging")

    except Table.DoesNotExist as e:
        logger.error("Somebody tried to get a menu for a non " +
                     "existing table: %s", table_uuid)
        raise Http404()

    # render the template
    return render(request, "menus/order.html", {'cat_menu_items': cat_menu_items,
                                                'place': place,
                                                'table_uuid': table_uuid})