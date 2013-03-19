from django.views.decorators.http import condition, require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages import warning
from django.utils import simplejson
from django.db.models import Q
from shoutcast import ShoutCastStream
from global_decorators import render_to, require_section_enabled
from models import Music


@condition(etag_func=None)
@require_section_enabled('music')
def stream(request):
    if Music.currently_playing() is not None:
        warning(request, "Only one Shoutcast stream may be active at any time")
        return HttpResponseRedirect("/")
    response = HttpResponse(ShoutCastStream(request))
    return response


@render_to('music_list.html')
@require_section_enabled('music')
def index(request):
    music_set = Music.objects.all()
    icon = "music"
    title = "Request A Song from the Library"
    return locals()


@require_POST
@require_section_enabled('music')
def search(request):
    search_string = request.POST.get('s','')
    results = Music.objects.filter(
        Q(artist__contains=search_string) |
        Q(title__contains=search_string)
    ).values('id','artist','title')
    data = simplejson.dumps(list(results))
    return HttpResponse(data, mimetype='application/json')


@require_POST
@require_section_enabled('music')
def request_song(request):
    try:
        song = Music.objects.get(id=request.POST.get('song'))
        song.request(request.user)
        return HttpResponse('{"success": true}', mimetype='application/json')
    except Music.DoesNotExist:
        return HttpResponse('{"success": false}', mimetype='application/json')


@require_section_enabled('music')
def current(request):
    playing = Music.currently_playing()
    data = {}
    if playing:
        data['artist'] = playing.artist
        data['title'] = playing.title
        if playing.associated_request is not None:
            data['requested_by'] = playing.associated_request.requester.username
        else:
            data['requested_by'] = "Random Play"

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')