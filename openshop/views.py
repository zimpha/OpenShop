from django.shortcuts import render
import re
# import json
import urllib2
import decimal
import chardet
import datetime
from django import forms
from openshop.models import *
from django.template import *
from bs4 import BeautifulSoup
#from forms import RegisterForm
from django.contrib import auth
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response,RequestContext
# Create your views here.


def hello(request):
    return HttpResponse("Hello world")

def helloParam(request, param1):
    return HttpResponse("The param is : " + param1)

def index(request):
    if request.user.is_authenticated():
        print 'login success'
    else:
        print 'login failure'
    return HttpResponse("hehe")

def login(request):
    if (request.method == 'POST'):
        print 'get post'
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not Node and user.is_active:
            auth.login(request, user)
            request.session["username"] = username
            user = User.objects.get(username = username)
            try:
                user.get_profile()
            except:
                profile = UserProfile(user = user)
                profile.save()
            print 'login success'
        else:
            print 'invaid user'
    else:
        print 'get'
        return HttpResponse('get method')

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/index")

def register(request):
    if request.method == 'POST':
        print 'post method'
        username = request.POST['username']
        password = request.POST['password']
        print username + " " + password
        try:
            user = User.objects.create_user(username, '', password)
            user.save()
            try:
                user.get_profile()
            except:
                profile = UserProfile(user = user)
                profile.save()
            print 'register success'
        except:
            return HttpResponse('user exists')
    else:
        print 'get method'
    return HttpResponse('register')

def add_card(request):
    return HttpResponse('add_card')

def search(request):
    return HttpResponse('search')

def profile(request):
    return HttpResponse('profile')

def order(request):
    return HttpResponse('order')