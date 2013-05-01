from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'servers.views.index'),
    url(r'^register/?', 'servers.views.register'),
    url(r'^info/(?P<server_id>\d+)/?$', 'servers.views.info')
)
