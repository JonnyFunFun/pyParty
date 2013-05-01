from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/?$', 'admin.news.views.index'),
    url(r'^new/?$', 'admin.news.views.new'),
    url(r'^news/(?P<news_id>\d+)/delete/?$', 'admin.news.views.delete')
)
