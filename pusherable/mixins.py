# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from pusher import Config, Pusher


class PusherMixin(object):
    pusher_include_model_fields = None
    pusher_exclude_model_fields = None
    
    def render_to_response(self, context, **response_kwargs):

        config = Config(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET
        )

        channel = u"{model}_{pk}".format(
            model=self.object._meta.model_name,
            pk=self.object.pk
        )
        
        data = self.__model_to_json_serializable(self.object)
        
        pusher = Pusher(config=config)
        pusher.trigger(
            [channel, ],
            self.pusher_event_name,
            {
                'model': data,
                'user': self.request.user.username
            }
        )

        return super(PusherMixin, self).render_to_response(context, **response_kwargs)
        
    def __model_to_json_serializable(self, model):
        model_dict = model_to_dict(self.object, 
                                   fields=self.pusher_include_model_fields, exclude=self.pusher_exclude_model_fields)
        json_data = json.dumps(model_dict, cls=DjangoJSONEncoder)
        data = json.loads(json_data)
        return data


class PusherUpdateMixin(PusherMixin):
    pusher_event_name = u"update"


class PusherDetailMixin(PusherMixin):
    pusher_event_name = u"view"
