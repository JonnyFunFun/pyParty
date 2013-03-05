from django.views.decorators.http import condition, require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages import warning
from django.utils import simplejson
from django.db.models import Q
from django.core import serializers
from shoutcast import ShoutCastStream
from global_decorators import render_to
from models import Music


@condition(etag_func=None)
def stream(request):
    if Music.currently_playing() is not None:
        warning(request, "Only one Shoutcast stream may be active at any time")
        return HttpResponseRedirect("/")
    response = HttpResponse(ShoutCastStream(request))
    return response


@render_to('request_home.html')
def index(request):
    return locals()


@require_POST
def search(request):
    search_string = request.POST.get('s','')
    results = Music.objects.filter(
        Q(artist__contains=search_string) |
        Q(title__contains=search_string)
    ).values('id','artist','title')
    data = simplejson.dumps(list(results))
    return HttpResponse(data, mimetype='application/json')


@require_POST
def request_song(request):
    try:
        song = Music.objects.get(id=request.POST.get('song'))
        song.request(request.user)
        return HttpResponse('{"success": true}', mimetype='application/json')
    except Music.DoesNotExist:
        return HttpResponse('{"success": false}', mimetype='application/json')


def current(request):
    playing = Music.currently_playing()
    if playing:
        data = '{"artist": "%s", "title": "%s"}' % (playing.artist, playing.title)
    else:
        data = '{}'
    return HttpResponse(data, mimetype='application/json')
