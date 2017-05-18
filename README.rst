=============================
django-pusherable
=============================

Real-time object access notifications via Pusher_

.. _Pusher: https://pusher.com

Installation
------------

Install django-pusherable::

    pip install django-pusherable


Configuration
-------------

Then add `pusherable` to your `INSTALLED_APPS`. You will also need to add your Pusher
app credentials to `settings.py`. These are available on your app keys page.::

    PUSHER_APP_ID = u""
    PUSHER_KEY = u""
    PUSHER_SECRET = u""
    PUSHER_CLUSTER = u""

Mixins
------

To begin receiving notifications about an object use the mixins.::

    from pusherable.mixins import PusherDetailMixin, PusherUpdateMixin

    class PostDetail(PusherDetailMixin, DetailView):
        model = Post

    class PostUpdate(PusherUpdateMixin, UpdateView):
        model = Post
        form_class = PostUpdateForm

When the view is accessed it will send an event on the channel
`modelname_pk` which contains a JSON representation of the object (model instance)
being accessed as well as the user.

The data will be in the form:

    {
      "object": {
        "question": "What's up?",
        "pub_date": "2013-08-08T11:16:24",
        "id": 1
      },
      "user": "admin"
    }

Which fields are included and excluded within the `object` is configurable via
`pusher_include_model_fields` and `pusher_exclude_model_fields`. For example,
the following would exclude the `pub_date` from the event payload:

    class PostUpdate(PusherUpdateMixin, UpdateView):
        model = Post
        form_class = PostUpdateForm
        pusher_exclude_model_fields = 'pub_date'

Template tags
-------------

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
            alert(data.user + "has begun to " + event + " " + data.model);
        }
    </script>

Running Tests
-------------

Pusherable comes with test requirements and a test runner.::

    pip install -r requirements-test.txt
    python runtests.py


Credits
-------

django-pusherable was built by `Aaron Bassett`_ for Pusher.

.. _Aaron Bassett: https://twitter.com/aaronbassett
