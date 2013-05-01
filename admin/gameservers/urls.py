from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.gameservers.views.index'),
    url(r'^(?P<server_id>\d+)?/?save/?$', 'admin.gameservers.views.save'),
    url(r'^add/?$', 'admin.gameservers.views.add'),
    url(r'^(?P<server_id>\d+)/edit/?$', 'admin.gameservers.views.edit'),
    url(r'^(?P<server_id>\d+)/delete/?$', 'admin.gameservers.views.delete'),
    url(r'^(?P<server_id>\d+)/alive/?$', 'admin.gameservers.views.alive'),
    url(r'^(?P<server_id>\d+)/approve/?$', 'admin.gameservers.views.approve'),
)
