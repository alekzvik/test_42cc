from django.conf.urls import patterns, url
# from contact.views import ContactUpdate
# from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', 'contact.views.index'),
    url(r'^edit/$', 'contact.views.contact_edit', name='contact_edit'),
)
