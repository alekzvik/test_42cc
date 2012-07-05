from django.conf.urls import patterns, url
from django.views.generic import ListView
from requests_log.models import RequestEntry

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=RequestEntry.objects.all()[:10],
        context_object_name='requests',
        template_name="requests.html"), name='requests_view'),
)
