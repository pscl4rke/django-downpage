

import logging
LOG = logging.getLogger(__name__)

import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string


def generate():
    LOG.debug("Started")
    pages_to_generate = get_pages_to_generate(settings)
    for filename, templatename in pages_to_generate:
        filepath = os.path.join(settings.STATIC_ROOT, filename)
        LOG.debug("Building %r..." % filepath)
        context = {"request": None}
        content = render_to_string(templatename, context)
        with open(filepath, "w") as destfile:
            destfile.write(content)
    LOG.debug("Finished")


def get_pages_to_generate(settings):
    if not hasattr(settings, "DOWNPAGE_PAGES"):
        raise ImproperlyConfigured("Missing DOWNPAGE_PAGES")
    return settings.DOWNPAGE_PAGES
