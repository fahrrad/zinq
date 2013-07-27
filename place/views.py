from django.shortcuts import render
from place.models import Place, Table
from menu.models import Menu, MenuItem


def welcome(request):
    return render(request, "place/welcome.html")

def menu(request, table_uuid):
    """Typicaly called from a mobile device when scanning a qr code.
     The second parameter is the unique place identifier. This corresponds to a
     table, and uniquely identies a menu
    """
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
