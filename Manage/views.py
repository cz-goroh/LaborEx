from django.shortcuts import render
from .tasks import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import logging
from django.contrib.auth import authenticate, login
# Create your views here.

# logging.basicConfig(filename="task_book.log", level=logging.INFO)

def index(request):
    # print(type(test1))
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
    if 'registr' in post:
        if not Person.objects.filter(email=post['email']):
            user = Person.objects.create_user(post['email'], post['email'],
                                              post['password'], position='user')
            user.save()
            user.is_staff = True
            user.save()
            login(request, user)

    test1.delay()
    # return HttpResponse('index')
    q={}
    return render(request, 'Manage/index.html', q)
