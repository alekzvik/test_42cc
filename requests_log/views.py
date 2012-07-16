from django.shortcuts import redirect, render
from requests_log.forms import RequestEntryFormSet
from django.contrib.auth.decorators import login_required
from requests_log.models import RequestEntry


def requests_view(request):
    requests = RequestEntry.objects.all()[:10]
    formset = RequestEntryFormSet(queryset=requests)
    objects = zip(requests, formset)
    return render(request, "requests.html", {'objects': objects, 'formset': formset})


@login_required
def priority_update(request):
    if request.method == 'POST':
        formset = RequestEntryFormSet(request.POST)

        if formset.is_valid():
            formset.save()

    return redirect('requests_view')
