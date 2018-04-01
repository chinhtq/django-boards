# -*- coding: UTF-8 -*-
# System libraries
from __future__ import unicode_literals
# Third-party libraries

# Django modules

# Current-app modules

# Other-app modules
import hashlib
from urllib import urlencode

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    print email
    default = 'mm'
    size = 256
    url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({'d': default, 's': str(size)}),
    )
    print 'md5',hashlib.md5(email).hexdigest()
    print 'params', urlencode({'d': default, 's': str(size)})

    return url