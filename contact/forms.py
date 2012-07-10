from django.forms import ModelForm
from contact.models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'last_name', 'birth_date', 'photo', 'email',
            'jabber', 'skype', 'other_contacts', 'bio')
