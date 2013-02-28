from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.music.views.index'),
    url(r'^source/add/?$', 'admin.music.views.add_source'),
    url(r'^source/(?P<source_id>\d+)/scan/do/?$', 'admin.music.views.do_scan'),
    url(r'^source/(?P<source_id>\d+)/scan/?$', 'admin.music.views.scan_source'),
)
