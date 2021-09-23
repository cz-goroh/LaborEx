from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    exclude = ['password', ]
    list_display = ['username', 'money', ]
    search_fields = ['username', 'email']


admin.site.register(Person, PersonAdmin)
