"""LaborEx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from Manage.views import index, ConfView, UserCabPage
from Blog.views import IndexView, RubricView, auth_form, ImplementerView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('Manage.urls')),
    path('order/', include('Order.urls')),

    path('conditions/', ConfView.as_view(), name='conditions'),
    path('confedence/', ConfView.as_view(), name='confedence'),
    path('implementer/', ImplementerView.as_view(), name='implementer'),
    # path('accounts/google/login/callback/', index, name='index_cab'),

    path('', IndexView.as_view(), name='index'),
    path('reflink/<str:code>/', index, name='reflink'),

    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('auth_form/', auth_form, name='auth_form'),

    path('rubric/<str:slug>', RubricView.as_view(), name='rubric'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.STATIC_URL)
urlpatterns += staticfiles_urlpatterns()
