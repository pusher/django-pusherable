from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def poan_script():
    return "<script src=\"//js.pusher.com/2.2/pusher.min.js\" type=\"text/javascript\"></script>"


@register.simple_tag
def poan_subscribe(event, instance):

    channel = u"{model}_{pk}".format(
        model=instance._meta.model_name,
        pk=instance.pk
    )

    return """
    <script type=\"text/javascript\">
    var pusher = new Pusher('{key}');
    var channel = pusher.subscribe('{channel}');
    channel.bind('{event}', function(data) {{
      poan_notify('{event}', data);
    }});
    </script>
    """.format(
        key=settings.PUSHER_KEY,
        channel=channel,
        event=event
    )
