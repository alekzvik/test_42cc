from django.conf.urls import patterns, url
from contact.views import ContactUpdate
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', 'contact.views.index'),
    url(r'^edit/$', login_required(ContactUpdate.as_view()),
        name='contact_edit'),
)
