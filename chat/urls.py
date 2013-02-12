from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'sync', 'chat.views.sync'),
    url(r'post', 'chat.views.post'),
)
