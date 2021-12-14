from django.shortcuts import render
import logging, asyncio, websockets, json
from django.views.generic import TemplateView, FormView, ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.cache import cache
from django.template.loader import render_to_string
from django.db.models import Q, Count, Subquery, F, OuterRef
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
    # print(request.POST)
    params = json.loads(request.POST['data'])
    offers = Offer.objects.all()
    orders = Order.objects.filter(status='new')
    price_from = (params['price_from'] or params['price_from-m'])
    if price_from:
        orders = orders.filter(price__gte=price_from)
    price_to = (params['price_to'] or params['price_to-m'])
    if price_to:
        orders = orders.filter(price__lte=price_to)
    union_qs = []
    qs_excl = []
    if params['online'] or params['online-m'] or params['offline'] or params['offline-m']:
        if (params['online'] or params['online-m']):
            # print('online')
            union_qs.append(orders.filter(rubric__type='online'))
        else:
            qs_excl.append(orders.filter(rubric__type='online'))
        if params['offline'] or params['offline-m']:
            # print('ofline')
            union_qs.append(orders.filter(rubric__type='ofline'))
        else:
            qs_excl.append(orders.filter(rubric__type='ofline'))
    is_budget = []
    budget_dict = {}
    is_offers = []
    offers_dict = {}
    for k, v in params.items():
        if len(k.split('_')) >= 2 and k.split('_')[0] == 'budget':
            is_v = (
                params[f"budget_{k.split('_')[1]}_{k.split('_')[2]}_"] or params[f"budget_{k.split('_')[1]}_{k.split('_')[2]}_-m"]
            )
            budget_dict[f"{k.split('_')[1]}_{k.split('_')[2]}"] = is_v
            if v:
                is_budget.append(v)
        elif len(k.split('_')) >= 2 and k.split('_')[0] == 'offers':
            is_o = (
                params[f"offers_{k.split('_')[1]}_{k.split('_')[2]}_"] or
                params[f"offers_{k.split('_')[1]}_{k.split('_')[2]}_-m"]
            )
            offers_dict[f"{k.split('_')[1]}_{k.split('_')[2]}"] = is_o
            if v:
                is_offers.append(v)
    if is_offers:
        orders = orders.annotate(
            orders_count=Count(Subquery(offers.filter(order=OuterRef('pk')).only('pk'))),
            # output_field=models.IntegerField()
        )
        for off_k, iso in offers_dict.items():
            count_query = orders.filter(
                Q(orders_count__gte=off_k.split('_')[0]) &
                Q(orders_count__lte=off_k.split('_')[1]))
            if iso:
                union_qs.append(count_query)
            else:
                qs_excl.append(count_query)
    # print(budget_dict)
    if is_budget:
        for bud_k, isv in budget_dict.items():
            if isv:
                union_qs.append(orders.filter(Q(price__gte=bud_k.split('_')[0]) &
                                              Q(price__lte=bud_k.split('_')[1])))
            else:
                qs_excl.append(orders.filter(Q(price__gte=bud_k.split('_')[0]) &
                                             Q(price__lte=bud_k.split('_')[1])))
    # for ok, ov in p
    orders = orders.difference(*qs_excl)
    orders = orders.union(*union_qs)
    # print('result_orders')
    # print(orders)
    q = {'object_list': orders}
    rend = render_to_string(
        'Order/order_list.html',
        {'object_list': orders}
        )
    return HttpResponse(rend)
    # return render(request, 'Order/order_list.html', q)


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
