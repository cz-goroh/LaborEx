import logging, requests, jwt, base64, json
from string import ascii_letters
from random import choice
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.conf import settings
from .tasks import *
from .models import *

# Create your views here.

logging.basicConfig(filename="manage_view.log", level=logging.INFO)

class CabinetTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return super(CabinetTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hi'] = 'hi'
        return context

class ChatView(CabinetTemplateView):
    template_name = 'Manage/admin/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs['chat_id'] == 0:
            # print('hi')
            pass
        else:
            dialog_user = Person.objects.filter(pk=kwargs['chat_id']).first()
            context['dialog_user'] = dialog_user
            # context['messages'] = Message.objects.filter(user_from=self.request.user).filter(user_to=dialog_user)
            context['messages'] = Message.objects.filter(
                (Q(user_from=self.request.user) & Q(user_to=dialog_user)) |
                (Q(user_from=dialog_user) & Q(user_to=self.request.user))
            )
        context['users'] = Person.objects.all().exclude(pk=self.request.user.id)
        return context

class UserCabPage(CabinetTemplateView):
    template_name = 'Manage/admin/user_cab.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ref_links'] = ReferalLink.objects.filter(parent=self.request.user)
        return context


def index(request, code=None):
    q={}
    # print(code)
    reflink = None
    if code:
        q['refcode'] = code
        reflink = ReferalLink.objects.filter(code=code)
    post = request.POST
    if 'auth' in post:
        login_us=False
        user = authenticate(
            request,
            username=post['email'],
            password=post['password']
        )
        if user is not None:
            login(request, user)
            login_us=True
            return HttpResponseRedirect('/manage/user_cab/')

    if 'registr' in post:
        if not Person.objects.filter(email=post['email']):
            user = Person.objects.create_user(post['email'], post['email'],
                                              post['password'], position='user')
            user.save()
            user.is_staff = True
            user.save()
            login(request, user)
            if reflink:
                reflink.child = user
                reflink.save()
                user.refer = reflink.parent
                user.save()
            return HttpResponseRedirect('/manage/user_cab/')

    # test1.delay()
    # return HttpResponse('index')
    return render(request, 'Manage/index.html', q)


def generate_ref_link(request):
    new_code = ''.join(choice(ascii_letters) for i in range(50))
    link = f"{new_code}"
    new_link = ReferalLink(code=new_code, parent=request.user)
    new_link.save()
    return JsonResponse({'link': link, 'code': new_code})


def google_get_key(request):
    if 'code' in request.GET:
        # print(request.GET['code'])
        url="https://oauth2.googleapis.com/token"
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'code': request.GET['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://proofex.ru/manage/google_get_key/'
            }
        r = requests.post(url, data=params)
        # print(r.json())
        rjs = r.json()
        parts = rjs['id_token'].split(".")
        # print(len(parts))
        payload = parts[1]
        padded = payload + "=" * (4 - len(payload) % 4)
        decoded = base64.b64decode(padded)
        user_info = json.loads(decoded)
        # {'iss': 'https://accounts.google.com', 'azp': '451474316104-omk0c1kq1fefm6faprl9116h655dt4jr.apps.googleusercontent.com', 'aud': '451474316104-omk0c1kq1fefm6faprl9116h655dt4jr.apps.googleusercontent.com', 'sub': '102754829692333344119', 'email': 'cz.goroh@gmail.com', 'email_verified': True, 'at_hash': 'Vg3Tq7dWGdwaDXXJ_yApQw', 'name': 'андрей лобков', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GjSrH96wel7McV-ZNybJ6bSem0XQ6ADL93BVF3s=s96-c', 'given_name': 'андрей', 'family_name': 'лобков', 'locale': 'ru', 'iat': 1634129279, 'exp': 1634132879}
        is_person = Person.objects.filter(
            Q(username=user_info['sub']) |
            Q(username=user_info['email']) |
            Q(email=user_info['email'])
        ).first()
        if is_person:
            login(request, is_person)
        else:
            new_pass = ''.join(choice(ascii_letters) for i in range(12))
            new_user = Person.objects.create_user(user_info['sub'], user_info['email'],
                                       new_pass)
            new_user.save()
            login(request, new_user)
        return HttpResponseRedirect('/manage/user_cab/')


        return HttpResponseRedirect('/')
    else:
        url =  f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri=https://proofex.ru/manage/google_get_key/&response_type=code&scope=profile email&"
        return HttpResponseRedirect(url)


class ConfView(TemplateView):
    template_name = 'Manage/conf_v.html'
