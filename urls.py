from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'admin/', include('admin.urls')),
    url(r'accounts/', include('accounts.urls')),
    url(r'benchmarks/', include('benchmark.urls')),
    url(r'chat/', include('chat.urls')),
    url(r'gallery/', include('gallery.urls')),
    url(r'music/', include('music.urls')),
    url(r'noms/', include('noms.urls')),
    url(r'servers/', include('servers.urls')),
    url(r'tournaments/', include('tournaments.urls')),
    url(r'notices/?', 'notices.get_notices'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'path': 'favicon.ico'}),
    # always do this, even in production
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^/?$', 'dashboard.views.index')
)