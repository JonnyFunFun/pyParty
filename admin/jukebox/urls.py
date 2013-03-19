from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.jukebox.views.index'),
    url(r'^source/add/?$', 'admin.jukebox.views.add_source'),
    url(r'^source/(?P<source_id>\d+)/scan/do/?$', 'admin.jukebox.views.do_scan'),
    url(r'^source/(?P<source_id>\d+)/scan/?$', 'admin.jukebox.views.scan_source'),
    url(r'^source/(?P<source_id>\d+)/?$', 'admin.jukebox.views.view_source'),
    url(r'^song/(?P<song_id>\d+)/delete/?$', 'admin.jukebox.views.delete_song'),
    url(r'^song/(?P<song_id>\d+)/edit/?$', 'admin.jukebox.views.edit_song'),
)
