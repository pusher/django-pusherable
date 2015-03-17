=============================
django-poan
=============================

Real time object access notifications via Pusher

Quickstart
----------

Install django-poan::

    pip install django-poan

Then add `poan` to your `INSTALLED_APPS`. You will also need to add your pusher
keys to your settings. These are available on your app keys page.::

    PUSHER_APP_ID = u""
    PUSHER_KEY = u""
    PUSHER_SECRET = u""

To begin receiving notifications about an object use the mixins.::

    from poan.mixins import PusherDetailMixin, PusherUpdateMixin

    class PostDetail(PusherDetailMixin, DetailView):
        model = Post

    class PostUpdate(PusherUpdateMixin, UpdateView):
        model = Post
        form_class = PostUpdateForm

When the view is accessed it will send an event on the channel
`modelname_pk` which contains some information about the object being
accessed as well as the user.

To subscribe to these events on your page you can use the templatetags.::

    {% load poan_tags %}

    {% poan_script %}

The `poan_script` tag will include the Pusher library. Place this in the
head of your page.::

    {% poan_subscribe 'update' object %}

The `poan_subscribe` tag will begin subscribe you to the channel for the
object. The first argument is the type of event you want to subscribe to.
The default events are `update` and `view`.

When a new event is received it will pass event type and data to a Javascript
function called `poan_notify`. Create this function and use it to alert your
users to the new event. For example::

    <script>
        function poan_notify(event, data) {
            alert(data.user + "has begun to " + event + " " + data.object);
        }
    </script>
