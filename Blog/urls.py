from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'Blog'

urlpatterns = [
    path('ajax_auth/', views.ajax_auth, name='ajax_auth'),
]
