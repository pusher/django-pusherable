# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import PusherableExampleDetail


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', PusherableExampleDetail.as_view(), name="example"),
]
