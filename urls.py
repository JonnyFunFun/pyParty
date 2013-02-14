from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'admin/', include('admin.urls')),# or include(admin.site.urls)),
    url(r'accounts/', include('accounts.urls')),
    url(r'chat/', include('chat.urls')),
    url(r'music/', include('music.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'path': 'favicon.ico'}),
    url(r'^/?$', 'dashboard.views.index')
)
# always do this, even in production
urlpatterns += staticfiles_urlpatterns()