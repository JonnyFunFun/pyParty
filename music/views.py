from django.views.decorators.http import condition
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages import warning
from shoutcast import ShoutCastStream
from models import Music


@condition(etag_func=None)
def stream(request):
    if Music.currently_playing() is not None:
        warning(request, "Only one Shoutcast stream may be active at any time")
        return HttpResponseRedirect("/")
    response = HttpResponse(ShoutCastStream(request))
    return response