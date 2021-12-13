from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'rubric']

admin.site.register(OrderFile)
admin.site.register(Order, OrderAdmin)
admin.site.register(Offer)
