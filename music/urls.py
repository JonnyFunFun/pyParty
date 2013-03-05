from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^stream/?', 'music.views.stream'),
    url(r'^search/?', 'music.views.search'),
    url(r'^request/?', 'music.views.request_song'),
    url(r'^current/?', 'music.views.current'),
    url(r'^$', 'music.views.index'),
)
