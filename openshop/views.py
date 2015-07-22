from django.shortcuts import render
import re
import json
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
    if (request.method == 'GET'):
        print 'get method'
        if 'username' in request.GET and 'password' in request.GET:
            username = request.GET['username']
            password = request.GET['password']
            print username
            print password
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                request.session["username"] = username
                user = User.objects.get(username = username)
                print "dd"
                user_profile = UserProfile.objects.get(user = user)
                print 'login success'
                result = user_profile.as_json()
                result['islogin'] = 'true'
                print result
                return HttpResponse(json.dumps(result))
            else:
                print 'invaid user'
                result = {'islogin':'false'}
                return HttpResponse(json.dumps(result))
        else:
            print 'username or password not provide'
            result = {'islogin':'false'}
            return HttpResponse(json.dumps(result))
    else:
        print 'post method'
        return HttpResponse('post')

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/index")

def register(request):
    if request.method == 'GET':
        print 'post method'
        username = request.GET['username']
        password = request.GET['password']
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
        print 'post method'
    return HttpResponse('register')

def add_card(request):
    print request.GET['username']
    print request.GET['card_no']
    print request.GET['card_pass']

    try:
        card = Bank.objects.get(card_number =request.GET['card_no'], password = request.GET['card_pass'])
    except:
        return HttpResponse('no such card')

    try:
        user = User.objects.get(username = request.GET['username'])
    except:
        return HttpResponse('no such user')

    try:
        user_profile = user.get_profile()
    except:
        user_profile = UserProfile(user = user)
    try:
        user_profile.cards = card
        user_profile.save()
    except:
        return HttpResponse('cards exists')

    return HttpResponse('add_card')

def search(request):
    if request.method == 'GET':
        if 'title' in request.GET:
            title = request.GET['title']
            records = Item.objects.filter(title__icontains = title)
            results = [ob.as_json() for ob in records]
            print results
            return HttpResponse(json.dumps(results))
        else:
            return item_list(request)
    else:
        return json.dumps([])
    return HttpResponse('search')

def profile(request):
    return HttpResponse('profile')

def item_list(request):
    records = Item.objects.all()
    results = [ob.as_json() for ob in records]
    print results
    return HttpResponse(json.dumps(results))

def order_list(request):
    print request.GET['username']
    try:
        user = User.objects.get(username = request.GET['username'])
    except:
        return HttpResponse('no such user')

    records = Order.objects.filter(buyer = user)

    results = [ob.as_json() for ob in records]
    print results
    return HttpResponse(json.dumps(results))

def complete_order(request):
    print request.GET['order_id']
    order_id = request.GET['order_id']
    try:
        order = Order.objects.get(order_id = order_id)
        order.is_complete = True
        order.save()
        return HttpResponse('success')
    except:
        print "no such order"
        return HttpResponse('failed')
    return HttpResponse('complete_order')

def order(request):
    return HttpResponse('order')

def upload(request):
    return HttpResponse('upload_pic')

def handle_uploaded_file(f):
    with open('../static/img/a.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)