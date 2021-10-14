from django.forms import ModelForm, FileInput
from .models import *

class NewOrderForm(ModelForm):
    # files = FileInput()s
    class Meta:
        model = Order
        fields = ['name', 'descr', 'rubric', 'files', 'price',]


class NewOfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['header', 'message', 'price', 'work_duration', 'payment_mode']
