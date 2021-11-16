from django.shortcuts import render
import logging
from django.views.generic import TemplateView, FormView, ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.cache import cache
from .models import *
from .forms import *


class OfferListView(ListView):
    model = Offer
    template_name = 'Order/offer_list.html'


class NewOfferFormView(FormView):
    template_name = 'Order/new_offer_form.html'
    success_url = '/order/order_list/'
    form_class = NewOfferForm

    def form_valid(self, form, *args, **kwargs):
        form.instance.order = Order.objects.get(pk=self.kwargs['order_id'])
        form.instance.worker = self.request.user
        self.object = form.save(commit=True)
        self.object.save()
        return super().form_valid(form)


class NewOrderFormView(FormView):
    template_name = 'Order/new_order.html'
    form_class = NewOrderForm
    success_url = '/order/new_order_succes/'

    def form_valid(self, form):
        form.instance.client = self.request.user
        self.object = form.save(commit=True)
        self.object.save()
        return super().form_valid(form)


class OrderList(ListView):
    template_name = 'Order/order_list.html'
    model = Order


class NewOrderSuccesView(TemplateView):
    template_name = 'Order/new_order_succes.html'


def accept_offer(request):
    offer = Offer.objects.filter(pk=request.POST['offer_accept']).first()
    if offer and offer.order.client == request.user:
        order = offer.order
        order.result_offer = offer
        order.save()
        order.status == 'offer_accepted'
        order.save()
        order.price = offer.price
        order.save()
    return HttpResponseRedirect('/order/')


def save_order_desc(request):
    request.session = request.POST['order_desc']
    return JsonResponse({'ord': 'hi'})
