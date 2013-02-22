from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'profile/edit/', 'accounts.views.edit_profile'),
    url(r'profile/save/', 'accounts.views.save_profile'),
    url(r'profile/', 'accounts.views.view_profile'),
    url(r'user/(?P<username>[-_\w\d]+)/', 'accounts.views.user'),
    url(r'^/?$', 'accounts.views.view_profile')
)
