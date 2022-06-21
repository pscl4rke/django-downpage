
So...
obviously you are a fantastic programmer who never writes a bug
and a fantastic systems administrator who never lets your app go down.
But what about the rest of us?

Sometimes the upstream app process (e.g. `gunicorn`)
that runs your
[Django](https://www.djangoproject.com/)
website goes down,
and your frontend webserver (e.g. `nginx`) has to serve a 502
error page to visitors.

This gives you three options:

* Just use whatever the default error pages are within frontend server.
They will be very ugly and embarrassing.

* Create custom error pages that match your site's styling.
Perhaps you deploy them out as `static` files and point your frontend
server at the right location.
This starts out great,
but as you change your site styling the static error pages will get
out of sync.
You will create work for yourself to keep them updated.

* Use this `django-downpage` project!
It provides a `downpagegenerate` command which can be run
just after running `collectstatic`.
It will build static error pages from templates.
They will always be up-to-date,
but will also be available as static resources even when
the app server goes down.

