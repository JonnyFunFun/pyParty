from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.tournaments.views.index'),
)
