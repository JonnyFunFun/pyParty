from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'profile/edit/', 'accounts.views.edit_profile'),
    url(r'profile/save/', 'accounts.views.save_profile'),
    url(r'profile/', 'accounts.views.view_profile'),
    url(r'user/(?P<username>[-_\w\d]+)/', 'accounts.views.user'),
    url(r'goodbye/?$', 'accounts.views.departing'),
    url(r'goodbye/finish/?$', 'accounts.views.do_departure'),
    url(r'^/?$', 'accounts.views.list_users')
)
