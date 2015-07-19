from django.conf.urls import patterns, include, url
from openshop.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import  logout

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/?$', index),
    url(r'^logout/?$', logout),
    url(r'^hello/?$', hello),
]