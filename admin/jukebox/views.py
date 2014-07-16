from django.db import IntegrityError
from global_decorators import render_to
from admin.decorators import admin_only
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from music.models import MusicSource, Music, Request
from admin.jukebox.forms import NewMusicSourceForm
from django.views.decorators.http import condition
from music.scanner import scan_media
from django.utils import simplejson
from os import path


@render_to('music_index.html')
@admin_only
def index(request, form=None):
    sources = MusicSource.objects.all()
    total_music = Music.objects.count()
    total_requests = Request.objects.count()
    outstanding_requests = Request.objects.filter(fulfilled=False).count()
    add_form = form or NewMusicSourceForm()
    icon = "music"
    title = "Music Administration"
    return locals()


@render_to('music_sourcelist.html')
@admin_only
def view_source(request, source_id):
    try:
        source = MusicSource.objects.get(id=source_id)
    except MusicSource.DoesNotExist:
        messages.error(request, "Unable to find the music source with id %s" % source_id)
        return HttpResponseRedirect('/admin/music/')
    icon = "music"
    title = "Music Administration"
    message = "Viewing music from %s" % source.path
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
    icon = "search"
    title = "Scanning for music..."
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


@admin_only
@require_POST
def delete_song(request, song_id):
    try:
        song = Music.objects.get(id=song_id)
    except Music.DoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "error": "Song not found"}), mimetype='application/json')
    song.delete()
    return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')


@admin_only
@require_POST
def edit_song(request, song_id):
    try:
        song = Music.objects.get(id=song_id)
    except Music.DoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "error": "Song not found"}), mimetype='application/json')
    # update it
    song.artist = request.POST.get('artist') if request.POST.get('artist').__len__() > 0 else song.artist
    song.album = request.POST.get('album') if request.POST.get('album').__len__() > 0 else song.album
    song.title = request.POST.get('title') if request.POST.get('title').__len__() > 0 else song.title
    try:
        song.save()
    except IntegrityError as err:
        return HttpResponse(simplejson.dumps({"success": False, "error": err.message}), mimetype='application/json')
    return HttpResponse(simplejson.dumps({"success": True}), mimetype='application/json')