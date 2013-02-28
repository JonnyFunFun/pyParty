from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'settings/save/', 'admin.views.save_settings'),
    url(r'settings/', 'admin.views.settings'),
    url(r'users/', include('admin.users.urls')),
    url(r'music/', include('admin.music.urls')),
    url(r'^/?$', 'admin.views.index'),
)
