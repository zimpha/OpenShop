import re
import json
import decimal
import chardet
import datetime
import random
from django import forms
from openshop.models import *
from django.template import *
from bs4 import BeautifulSoup
# from forms import RegisterForm
from django.contrib import auth
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, RequestContext


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
    if request.method == 'GET':
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
                user = User.objects.get(username=username)
                print "dd"
                user_profile = UserProfile.objects.get(user=user)
                print 'login success'
                result = user_profile.as_json()
                result['islogin'] = 'true'
                print result
                return HttpResponse(json.dumps(result))
            else:
                print 'invaid user'
                result = {'islogin': 'false'}
                return HttpResponse(json.dumps(result))
        else:
            print 'username or password not provide'
            result = {'islogin': 'false'}
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
                profile = UserProfile(user=user)
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
        card = Bank.objects.get(card_number=request.GET['card_no'], password=request.GET['card_pass'])
    except:
        return HttpResponse('no such card')

    try:
        user = User.objects.get(username=request.GET['username'])
    except:
        return HttpResponse('no such user')

    try:
        user_profile = user.get_profile()
    except:
        user_profile = UserProfile(user=user)
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
            records = Item.objects.filter(title__icontains=title)
            results = [ob.as_json() for ob in records]
            results.sort(key=lambda x:x['item_id'],reverse=True)
            print results
            return HttpResponse(json.dumps(results))

        if 'item_id' in request.GET:
            item_id = request.GET['item_id']
            try:
                record = Item.objects.get(id=item_id)
                print record
                return HttpResponse(json.dumps(record.as_json()))
            except:
                return json.dumps([])

        if 'catalog' in request.GET:
            catalog = request.GET['catalog']
            records = Item.objects.filter(catalog=catalog)
            results = [ob.as_json() for ob in records]
            results.sort(key=lambda x:x['item_id'],reverse=True)
            print results
            return HttpResponse(json.dumps(results))
        if 'username' in request.GET:
            username = request.GET['username']
            try:
                user = User.objects.get(username=username)
            except:
                return HttpResponse(json.dumps([]))
            records = Item.objects.filter(publisher=user)
            results = [ob.as_json() for ob in records]
            results.sort(key=lambda x:x['item_id'],reverse=True)
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
    results.sort(key=lambda x:x['item_id'],reverse=True)
    print results
    return HttpResponse(json.dumps(results))


def add_item(request):
    if 'username' not in request.GET or request.GET['username'] == '':
        return HttpResponse(json.dumps(dict(result='no username')))
    if 'title' not in request.GET or request.GET['title'] == '':
        return HttpResponse(json.dumps(dict(result='no title')))
    if 'description' not in request.GET or request.GET['description'] == '':
        return HttpResponse(json.dumps(dict(result='no description')))
    if 'quantity' not in request.GET or request.GET['quantity'] == '':
        return HttpResponse(json.dumps(dict(result='no quantity')))
    if 'price' not in request.GET or request.GET['price'] == '':
        return HttpResponse(json.dumps(dict(result='no price')))
    if 'catalog' not in request.GET or request.GET['catalog'] == '':
        return HttpResponse(json.dumps(dict(result='no catalog')))

    username = request.GET['username']
    title = request.GET['title']
    des = request.GET['description']
    try:
        quantity = int(request.GET['quantity'])
    except:
        return HttpResponse(json.dumps(dict(result='quantity must be a number')))
    try:
        price = float(request.GET['price'])
    except:
        return HttpResponse(json.dumps(dict(result='price must be a number')))
    catalog = request.GET['catalog']

    try:
        user = User.objects.get(username = username)
    except:
        return HttpResponse(json.dumps(dict(result='no such user')))
    item = Item()
    item.publisher = user
    item.title = title
    item.description = des
    item.quantity = quantity
    item.price = price
    item.catalog = catalog
    item.start_time = datetime.datetime.now()
    item.end_time = datetime.datetime.now()
    item.save()
    return HttpResponse(json.dumps(dict(result='success')))


def order_list(request):
    if 'username' not in request.GET or request.GET['username'] == '':
        return HttpResponse(json.dumps(dict(result='no username')))
    if 'type' not in request.GET or request.GET['type'] == '':
        return HttpResponse(json.dumps(dict(result='no type')))
    type = request.GET['type']
    username = request.GET['username']
    print type + ' ' + username
    if type not in ['buyer', 'seller']:
        return HttpResponse(json.dumps(dict(result='no such type')))
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse('no such user')

    if type == 'buyer':
        records = Order.objects.filter(buyer=user)
    else:
        records = Order.objects.filter(seller=username)

    results = [ob.as_json() for ob in records]
    results.sort(key=lambda x:x['order_id'],reverse=True)
    print results
    return HttpResponse(json.dumps(results))


def complete_order(request):
    if 'order_id' not in request.GET['order_id']:
        return HttpResponse(json.dumps(dict(result='no order_id')))
    order_id = request.GET['order_id']
    print order_id
    try:
        order = Order.objects.get(order_id=order_id)
        order.is_complete = True
        order.save()
        return HttpResponse(json.dumps(dict(result='success')))
    except:
        print "no such order"
        return HttpResponse(json.dumps(dict(result='no such order')))


def order(request):
    if 'username' not in request.GET or request.GET['username'] == '':
        return HttpResponse(json.dumps(dict(result='no username')))
    if 'item_id' not in request.GET or request.GET['item_id'] == '':
        return HttpResponse(json.dumps(dict(result='no item_id')))
    if 'quantity' not in request.GET or request.GET['quantity'] == '':
        return HttpResponse(json.dumps(dict(result='no quantity')))
    username = request.GET['username']
    item_id = request.GET['item_id']
    try:
        quantity = int(request.GET['quantity'])
    except:
        return HttpResponse(json.dumps(dict(result='quantity must be a number')))
    try:
        item = Item.objects.get(id=item_id)
    except:
        return HttpResponse(json.dumps(dict(result='no item')))
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse(json.dumps(dict(result='no user')))
    item.quantity -= quantity
    if item.quantity < 0:
        return HttpResponse(json.dumps(dict(result='no enough quantity')))
    item.save()

    order = Order()
    order.quantity = quantity
    order.price = quantity * item.price
    order.buyer = user
    order.seller = item.publisher.username
    order.item = item
    order.order_time = datetime.datetime.now()
    order.is_set = False
    order.is_paid = False
    order.is_complete = False
    order.box_id = random.randint(1, 10)
    order.save()

    return HttpResponse(json.dumps(dict(result='success')))


def pay(request):
    if 'order_id' not in request.GET or request.GET['order_id'] == '':
        return HttpResponse(json.dumps(dict(result='no order_id')))
    if 'cpassword' not in request.GET or request.GET['cpassword'] == '':
        return HttpResponse(json.dumps(dict(result='no password')))
    order_id = request.GET['order_id']
    try:
        order = Order.objects.get(id = order_id)
    except:
        return HttpResponse(json.dumps(dict(result='no such order')))

    if order.is_paid:
        return HttpResponse(json.dumps(dict(result='already paid')))

    buyer = order.buyer
    seller = order.item.publisher
    buyer_profile = UserProfile.objects.get(user = buyer)
    seller_profile = UserProfile.objects.get(user = seller)
    buyer_card = buyer_profile.cards
    if buyer_card.password != request.GET['cpassword']:
        return HttpResponse(json.dumps(dict(result='bank password error')))
    seller_card = seller_profile.cards
    if buyer_card.balance < order.price:
        return HttpResponse(json.dumps(dict(result='no enough money')))

    buyer_card.balance -= float(order.price)
    seller_card.balance += float(order.price)
    order.is_paid = True
    buyer_card.save()
    seller_card.save()
    order.save()
    print 'ok'
    return HttpResponse(json.dumps(dict(result='success')))


def upload(request):
    return HttpResponse('upload_pic')


def handle_uploaded_file(f):
    with open('../static/img/a.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
