from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'stream', 'music.views.stream'),
)
