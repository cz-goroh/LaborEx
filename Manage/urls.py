from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'Manage'

urlpatterns = [
    path('user_cab/', views.UserCabPage.as_view(), name='user_cab'),
    path('labor_cab_page/', views.LaborCabPage.as_view(), name='labor_cab_page'),
    path('user_chat/<int:chat_id>/', views.ChatView.as_view(),
         name='user_chat'),

    path('google_get_key/', views.google_get_key, name='google_get_key'),

    path('generate_ref_link/', views.generate_ref_link,
         name='generate_ref_link'),

]
