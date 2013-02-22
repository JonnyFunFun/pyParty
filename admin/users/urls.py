from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<user_id>\d+)/delete/?$', 'admin.users.views.delete'),
    url(r'^(?P<user_id>\d+)/save/?$', 'admin.users.views.save'),
    url(r'^(?P<user_id>\d+)/?$', 'admin.users.views.edit'),
    url(r'^/?$', 'admin.users.views.index'),
)
