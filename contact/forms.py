from django.forms import ModelForm, DateInput
from contact.models import Contact


class CalendarWidget(DateInput):
    class Media:
        css = {
            'all': ('css/jquery-ui-1.8.21.custom.css', )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
            'js/jquery-ui-1.8.21.custom.min.js',
            'js/calendar.js',
        )


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'last_name', 'birth_date', 'photo', 'email',
            'jabber', 'skype', 'other_contacts', 'bio')
        widgets = {
            'birth_date': CalendarWidget(),
        }

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
            'js/contact_form.js'
        )
