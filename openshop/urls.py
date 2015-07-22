from django.conf.urls import patterns, include, url
from openshop.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import  logout

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/?$', index),
    url(r'^login/?$', login),
    url(r'^logout/?$', logout),
    url(r'^register/?$', register),
    url(r'^order_list/?$', order_list),
    url(r'^item_list/?$', item_list),
    url(r'^search/?$', search),
#    url(r'^add_card/?$', add_card),
    url(r'^complete_order/?$', complete_order),
    url(r'^hello/?$', hello),
]