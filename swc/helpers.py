# jingo template helpers to map any needed django template tags

import hashlib
import urllib

from django.conf import settings

from jingo import register


@register.function
def gravatar_url(email, size=80):
    return "http://www.gravatar.com/avatar/" + \
            hashlib.md5(email.lower()).hexdigest() + "?" + \
            urllib.urlencode({'d':'blank', 's':str(size)})


@register.function
def gravatar(email, size=80, options=""):
    url = gravatar_url(email, size)
    return '<img src="%s" width="%s" height="%s" %s />'%(url, size, size, options)

