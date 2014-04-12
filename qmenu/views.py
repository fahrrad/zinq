# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response

import logging
from django.template import RequestContext
from django.template.loader import get_template

logger = logging.getLogger(__name__)


def auth_login(request):
    """login a user"""
    if request.POST:
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                logger.info("Logging %s in" % username)
                login(request, user)
                # redirect to same page
                return redirect(request.path)
            else:
                logger.warn("User %s is not active", username)
                return render_to_response("places/error")
        else:
            logger.warn("User %s and password not correct", username)
            return render_to_response("places/error.html",
                                      {'error_msg': "User %s and password not correct" % username})
    else:
        logger.info("Login first, then go to %s", request.GET['next'])
        c = RequestContext(request, {'next:': request.GET['next']})
        t = get_template("places/login.html")
        return HttpResponse(t.render(c))


def auth_logout(request):
    logout(request)

    return redirect("/")

