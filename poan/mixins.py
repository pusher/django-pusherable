# -*- coding: utf-8 -*-

from django.conf import settings
from pusher import Config, Pusher


class PusherMixin(object):
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

        pusher = Pusher(config=config)
        pusher.trigger(
            [channel, ],
            self.pusher_event_name,
            {'user': self.request.user.username}
        )

        return super(PusherMixin, self).render_to_response(context, **response_kwargs)


class PusherUpdateMixin(PusherMixin):
    pusher_event_name = u"update"


class PusherDetailMixin(PusherMixin):
    pusher_event_name = u"view"
