from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'requests_log.views.requests_view', name='requests_view'),
    url(r'^priority_update/$', 'requests_log.views.priority_update'),
)
