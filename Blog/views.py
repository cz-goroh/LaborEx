from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache
from Manage.models import *
from .models import *


class MyTemplate(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_rubrics'] = Rubric.objects.filter(parent__isnull=True)
        return context


class IndexView(MyTemplate):
    template_name = 'Blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ImplementerView(MyTemplate):
    template_name = 'Blog/implementer.html'


class RubricView(MyTemplate):
    template_name = 'Blog/rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.get(slug = kwargs['slug'])
        return context


def auth_form(request):
    login_us=False
    post = request.POST
    # print(request.POST)
    user = authenticate(
        request,
        username=post['email'],
        password=post['password']
    )
    if user is not None:
        login(request, user)
        login_us=True
        return HttpResponseRedirect('/manage/user_cab/')
    return HttpResponseRedirect('/')


def ajax_auth(request):
    post = request.POST
    user = authenticate(
        request,
        username=post['email'],
        password=post['password']
    )
    if user is not None:
        login(request, user)
        return JsonResponse({'auth': True, 'user': user.id})
    return JsonResponse({'auth': False})

def registration(request):
    return HttpResponseRedirect('/')
