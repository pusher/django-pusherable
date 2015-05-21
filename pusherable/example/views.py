# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from pusherable.mixins import PusherDetailMixin
from .models import PusherableExample


class PusherableExampleDetail(PusherDetailMixin, DetailView):
    model = PusherableExample
    template_name = "example.html"
