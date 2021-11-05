from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

app_name = 'Order'

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offers'),
    path('new_order/', NewOrderFormView.as_view(), name='new_order'),
    path('new_order_succes/', NewOrderSuccesView.as_view(),
         name='new_order_succes'),
    path('order_list/', OrderList.as_view(), name='order_list'),
    path('new_offer_form/<int:order_id>/', NewOfferFormView.as_view(), name='new_offer_form'),

    path('save_order_desc/', save_order_desc, name='save_order_desc'),

    path('', OrderList.as_view())
]
