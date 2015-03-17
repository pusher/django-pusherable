=============================
django-pusherable
=============================

Real time object access notifications via Pusher

Quickstart
----------

Install django-pusherable::

    pip install django-pusherable

Then add `pusherable` to your `INSTALLED_APPS`. You will also need to add your pusher
keys to your settings. These are available on your app keys page.::

    PUSHER_APP_ID = u""
    PUSHER_KEY = u""
    PUSHER_SECRET = u""

To begin receiving notifications about an object use the mixins.::

    from pusherable.mixins import PusherDetailMixin, PusherUpdateMixin

    class PostDetail(PusherDetailMixin, DetailView):
        model = Post

    class PostUpdate(PusherUpdateMixin, UpdateView):
        model = Post
        form_class = PostUpdateForm

When the view is accessed it will send an event on the channel
`modelname_pk` which contains some information about the object being
accessed as well as the user.

To subscribe to these events on your page you can use the templatetags.::

    {% load pusherable_tags %}

    {% pusherable_script %}

The `pusherable_script` tag will include the Pusher library. Place this in the
head of your page.::

    {% pusherable_subscribe 'update' object %}

The `pusherable_subscribe` tag will begin subscribe you to the channel for the
object. The first argument is the type of event you want to subscribe to.
The default events are `update` and `view`.

When a new event is received it will pass event type and data to a Javascript
function called `pusherable_notify`. Create this function and use it to alert your
users to the new event. For example::

    <script>
        function pusherable_notify(event, data) {
            alert(data.user + "has begun to " + event + " " + data.object);
        }
    </script>
