from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.music.views.index'),
    url(r'^source/add/?$', 'admin.music.views.add_source'),
    url(r'^source/(?P<source_id>\d+)/scan/do/?$', 'admin.music.views.do_scan'),
    url(r'^source/(?P<source_id>\d+)/scan/?$', 'admin.music.views.scan_source'),
    url(r'^source/(?P<source_id>\d+)/?$', 'admin.music.views.view_source'),
    url(r'^song/(?P<song_id>\d+)/delete/?$', 'admin.music.views.delete_song'),
    url(r'^song/(?P<song_id>\d+)/edit/?$', 'admin.music.views.edit_song'),
)
