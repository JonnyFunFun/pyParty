from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include('admin.urls')),# or include(admin.site.urls)),
    url(r'accounts/', include('userena.urls')),
    url(r'chat/', include('chat.urls')),
    url(r'', 'dashboard.views.index')
)
