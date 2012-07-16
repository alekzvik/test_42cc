from django.forms.models import modelformset_factory

from requests_log.models import RequestEntry
from django import forms


class PriorityForm(forms.ModelForm):
    class Meta:
        model = RequestEntry
        fields = ('priority',)
        widgets = {
            'priority': forms.RadioSelect(),
        }


RequestEntryFormSet = modelformset_factory(
    RequestEntry,
    form=PriorityForm,
    fields=('priority',),
    extra=0
)
