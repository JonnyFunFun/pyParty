from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'settings/save/', 'admin.views.save_settings'),
    url(r'settings/', 'admin.views.settings'),
    url(r'users/', include('admin.users.urls')),
    url(r'music/', include('admin.jukebox.urls')),
    url(r'servers/', include('admin.gameservers.urls')),
    url(r'notices/?$', 'admin.views.notices'),
    url(r'^/?$', 'admin.views.index'),
)
