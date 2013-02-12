from django.views.decorators.http import condition
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.views.decorators.http import require_POST
from shoutcast import ShoutCastStream, CHUNKSIZE
from scanner import scan_media

@condition(etag_func=None)
def stream(request):
    shoutcast = ShoutCastStream()
    response = HttpResponse(shoutcast, content_type='audio/mpeg')
    # set our headers
    response['icy-notice1'] = "<BR>This stream requires"
    response['icy-notice2'] = "Winamp, or another streaming media player<BR>"
    response['icy-name'] = "pyParty ShoutCast"
    response['icy-genre'] = "Mixed"
    response['icy-url'] = resolve(request.path_info).url_name
    response['icy-pub'] = "1"
    response['icy-metaint'] = str(CHUNKSIZE)
    response['icy-br'] = "128"
    return response

@condition(etag_func=None)
@require_POST
def rescan(request):
    return HttpResponse(scan_media(), content_type='text/html')