from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.news.views.index'),
    url(r'^save/?$', 'admin.news.views.save'),
    url(r'^(?P<news_id>\d+)/delete/?$', 'admin.news.views.delete')
)
