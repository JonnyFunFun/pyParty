from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.tournaments.views.index'),
    url(r'^(?P<tournament_id>\d+)/delete/?$', 'admin.tournaments.views.delete'),
    url(r'^save/?$', 'admin.tournaments.views.save')
)
