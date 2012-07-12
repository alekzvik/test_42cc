from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from contact.forms import ContactForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings


def index(request):
    contact = get_object_or_404(Contact)
    return render(request, 'index.html', {'contact': contact})


@login_required
def contact_edit(request):

    if request.is_ajax():  # only if AJAX
        if getattr(settings, 'DEBUG', False):  # only if DEBUG=True
            import time
            time.sleep(1)

    contact = get_object_or_404(Contact)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)  # initial=contact.__dict__
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse("redirect")
            else:
                return redirect(reverse('contact.views.index'))
    else:
        # form = ContactForm(initial=contact.__dict__)
        form = ContactForm(instance=contact)
    return render(request, 'contact_edit.html', {'form': form})
