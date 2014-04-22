import logging

from django.shortcuts import render

from places.models import Place


logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, "places/welcome.html")


def landing(request):
    return render(request, 'landing.html')


def qr_codes(request, place_id):
    """Renders a view containing a QR code for every table in the places!"""
    host_prefix = "HTTP://stormy-peak-3604.herokuapp.com/MENU/"
    # host_prefix = "http://192.168.0.178:8000/menu/"
    try:
        place = Place.objects.get(pk=int(place_id))
    except place.DoesNotExist:
        return render(request, "places/error.html",
                      {'error_msg': "No place found with id %s!" % place_id})
    table_qr_list = [host_prefix + x.pk + "/" for x in place.table_set.all()]

    return render(request, "places/qr_codes.html", {'table_qr_list': table_qr_list,
                                                    'place_name': place.name})
