#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import mock

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.core.urlresolvers import reverse
from pusherable.mixins import PusherMixin
from pusherable.example.models import PusherableExample
from pusherable.example.views import PusherableExampleDetail


class TestPusherable(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='pusher', email='pusher@example.com', password='hunter2'
        )
        self.object = PusherableExample.objects.create(
            text = "This is a test PusherableExample object"
        )

    @mock.patch("pusherable.mixins.Pusher")
    def test_pusher_templatetags(self, Pusher):
        request =  self.factory.get(reverse("example", kwargs={"pk": self.object.pk}))
        request.user = self.user
        response = PusherableExampleDetail.as_view()(request, pk=self.object.pk)

        channel = u"{model}_{pk}".format(
            model=self.object._meta.model_name,
            pk=self.object.pk
        )

        self.assertContains(response, "js.pusher.com/2.2/pusher.min.js")
        self.assertContains(response, "pusher.subscribe('{channel}');".format(
            channel=channel
        ))