from global_decorators import render_to
from admin.decorators import admin_only
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from music.models import MusicSource, Music, Request
from forms import NewMusicSourceForm
from django.views.decorators.http import condition
from music.scanner import scan_media
from os import path


@render_to('music_index.html')
@admin_only
def index(request, form=None):
    sources = MusicSource.objects.all()
    total_music = Music.objects.count()
    total_requests = Request.objects.count()
    outstanding_requests = Request.objects.filter(fulfilled=False).count()
    add_form = form or NewMusicSourceForm()
    return locals()


@admin_only
@require_POST
def add_source(request):
    add_form = NewMusicSourceForm(data=request.POST)
    if add_form.is_valid() and path.exists(request.POST.get('path')):
        source = add_form.save()
        return HttpResponseRedirect('/admin/music/source/%s/scan/' % source.id)
    else:
        messages.error(request, "Please correct your errors and try again.")
    return index(request, add_form)


@render_to('scan_source.html')
@admin_only
def scan_source(request, source_id):
    try:
        source = MusicSource.objects.get(id=source_id)
    except MusicSource.DoesNotExist:
        messages.error(request, "Unable to find the music source with id %s" % source_id)
        return HttpResponseRedirect('/admin/music/')
    return locals()


@condition(etag_func=None)
@admin_only
def do_scan(request, source_id):
    resp = HttpResponse(scan_media(source_id), content_type='text/html')
    return resp

