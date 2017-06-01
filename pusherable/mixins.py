# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from pusher import Pusher


class PusherMixin(object):
    pusher_include_model_fields = None
    pusher_exclude_model_fields = None

    def render_to_response(self, context, **response_kwargs):

        channel = u"{model}_{pk}".format(
            model=self.object._meta.model_name,
            pk=self.object.pk
        )

        data = self.__object_to_json_serializable(self.object)

        try:
            pusher_cluster = settings.PUSHER_CLUSTER
        except AttributeError:
            pusher_cluster = 'mt1'

        pusher = Pusher(app_id=settings.PUSHER_APP_ID,
                        key=settings.PUSHER_KEY,
                        secret=settings.PUSHER_SECRET,
                        cluster=pusher_cluster)
        pusher.trigger(
            [channel, ],
            self.pusher_event_name,
            {
                'object': data,
                'user': self.request.user.username
            }
        )

        return super(PusherMixin, self).render_to_response(context, **response_kwargs)

    def __object_to_json_serializable(self, object):
        model_dict = model_to_dict(object,
                                   fields=self.pusher_include_model_fields, exclude=self.pusher_exclude_model_fields)
        json_data = json.dumps(model_dict, cls=DjangoJSONEncoder)
        data = json.loads(json_data)
        return data


class PusherUpdateMixin(PusherMixin):
    pusher_event_name = u"update"

class PusherDetailMixin(PusherMixin):
    pusher_event_name = u"view"

class PusherDeleteMixin(PusherMixin):
    pusher_event_name = u"delete"
