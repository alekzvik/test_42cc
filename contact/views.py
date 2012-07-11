from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from contact.forms import ContactForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def index(request):
    contact = get_object_or_404(Contact)
    return render(request, 'index.html', {'contact': contact})


@login_required
def contact_edit(request):
    contact = get_object_or_404(Contact)
    if request.method == 'POST':
        form = ContactForm(request.POST)  # initial=contact.__dict__
        if form.is_valid():
            contact.name = form.cleaned_data['name']
            contact.last_name = form.cleaned_data['last_name']
            contact.last_name = form.cleaned_data['last_name']
            contact.birth_date = form.cleaned_data['birth_date']
            contact.email = form.cleaned_data['email']
            contact.jabber = form.cleaned_data['jabber']
            contact.skype = form.cleaned_data['skype']
            contact.bio = form.cleaned_data['bio']
            contact.other_contacts = form.cleaned_data['other_contacts']
            contact.photo = form.cleaned_data['photo']
            contact.save()
            if request.is_ajax():
                return HttpResponse("redirect")
            else:
                return redirect(reverse('contact.views.index'))
    else:
        form = ContactForm(initial=contact.__dict__)
    return render(request, 'contact_edit.html', {'form': form})
