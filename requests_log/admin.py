from django.contrib import admin
from requests_log.models import RequestEntry

admin.site.register(RequestEntry)
