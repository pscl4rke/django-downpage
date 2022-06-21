

import logging
LOG = logging.getLogger(__name__)

import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string


def generate():
    if not hasattr(settings, "DOWNPAGE_PAGES"):
        raise ImproperlyConfigured("Missing DOWNPAGE_PAGES")
    LOG.debug("Started")
    for filename, templatename in settings.DOWNPAGE_PAGES:
        filepath = os.path.join(settings.STATIC_ROOT, filename)
        LOG.debug("Building %r..." % filepath)
        context = {"request": None}
        content = render_to_string(templatename, context)
        with open(filepath, "w") as destfile:
            destfile.write(content)
    LOG.debug("Finished")
