from django.shortcuts import render
import logging, asyncio, websockets, json
from django.views.generic import TemplateView, FormView, ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.cache import cache
from django.template.loader import render_to_string
from .models import *
from .forms import *


async def send_to_exchange_list(order):
    async with websockets.connect("ws://localhost:8080/ws/chat/") as websocket:
        await websocket.send(json.dumps(order))

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

        rendered_new_order_block = render_to_string(
            'Order/order_card_widget.html',
            {'order': self.object}
            )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(
            send_to_exchange_list({
                'new_order': self.object.id,
                'status': self.object.status,
                'name': self.object.name,
                'descr': self.object.descr,
                'rubric': self.object.rubric.name,
                'price': int(round(self.object.price)),
                # 'user_from': self.object.client.id,
                'rendered': rendered_new_order_block,
                })
        ))
        loop.close()
        return super().form_valid(form)


def ajax_filter_exchange(request):
    q = {}

    return render(request, 'Order/order_list.html', q)


class OrderList(ListView):
    """Биржа проектов"""
    template_name = 'Order/exchange.html'
    model = Order
    queryset = Order.objects.filter(status='new').order_by('-id')


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
