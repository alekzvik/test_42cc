from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from contact.models import Contact
from contact.forms import ContactForm
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse


def index(request):
    info = get_object_or_404(Contact)
    return render_to_response('index.html', {'info': info},
        context_instance=RequestContext(request))


class ContactUpdate(UpdateView):
    model = Contact
    queryset = get_object_or_404(Contact)
    form_class = ContactForm
    context_object_name = 'contact'
    # success_url = reverse('contact.views.index')
    template_name = 'contact_edit.html'

    def get_success_url(self):
        return reverse('contact.views.index')
