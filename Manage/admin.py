from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    exclude = ['password', ]
    list_display = ['username', 'money', 'email']
    search_fields = ['username', 'email']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'sent_time']


class RubricAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


admin.site.register(Person, PersonAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(ReferalLink)
# admin.site.register()
