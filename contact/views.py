from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from contact.models import Contact


def index(request):
    info = get_object_or_404(Contact)
    return render_to_response('index.html', {'info': info},
        context_instance=RequestContext(request))
