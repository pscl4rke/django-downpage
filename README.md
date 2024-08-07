
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

Usage:
------

Before starting it is recommended to ensure that `handler404`
and `handler500` error pages have already been configured
(as documented
[here](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views)
and [here](https://docs.djangoproject.com/en/dev/ref/urls/)).
Your templates from these views can serve as the basis for the
templates that `downpage` will use.

Install `django-downpage` from PyPI as with any
other dependency.
To quickly get started you might run:

    $ pip install django-downpage

although for production usage it would be more manageable to use
a `requirements.txt` or equivalent.

Now edit your `settings.py` to ensure `downpage` is listed
as an installed app.
The order is not significant:

    INSTALLED_APPS = [
        # ...snip...
        "downpage",
        # ...snip...
    ]

Also in `settings.py` you will need to define the list of pages
that should be built:

    DOWNPAGE_PAGES = [
        ("502.html", "myapp/downpage_502.html"),
        ("503.html", "myapp/downpage_503.html", {"name", "Service Unavailable"}),
        ("504.html", "myapp/downpage_504.html"),
        # ...etc...
    ]

The first element of the tuple is the destination file that will
get built, relative to the `STATIC_ROOT` directory.
The second element is the template name,
and is compatible with any name that can be understood by
the `render(...)` function that is a
[built-in shortcut](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#render).
An optional third element defines extra context that will be supplied
to the template when it is rendered.

At this point you need to create your templates.
A good starting point would be the pages served up for 404 or 500 errors.
You can use the same template for each generated page if you wish,
using extra context to customise them.
Also, if you have already set your site up to support the
[new-style Jinja2 templates](https://docs.djangoproject.com/en/dev/topics/templates/#django.template.backends.jinja2.Jinja2)
then they will work with no extra configuration needed.

Now update whatever process you use for deployment.
You presumably already call `manage.py collectstatic` as part of
this process.
The `downpagegenerate` management command is best run immediately after this:

    # ...snip...
    /path/to/virtualenv/bin/python manage.py collectstatic
    /path/to/virtualenv/bin/python manage.py downpagegenerate
    # ...snip...

Then you need to set up your frontend server to be aware of these files.
That will vary depending on the server you use.

Example: Configuring an Nginx Frontend:
---------------------------------------

If your frontend webserver is Nginx then you presumably already
have some config that looks something like this:

    location /static {
        alias /path/to/static.collected/;
    }

    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
    }

So add in an `error_page` directive for each type of error that
you want to handle:

    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
        error_page 502 /static/502.html;
        error_page 503 /static/503.html;
        error_page 504 /static/504.html;
    }

Postscript:
-----------

This code is licensed under the BSD three-clause licence.


