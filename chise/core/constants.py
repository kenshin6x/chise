# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


REQUEST_GET = 1
REQUEST_POST = 2
REQUEST_PARAM = 3
REQUEST_CHOICES = (
        (REQUEST_GET, _('GET')),
        (REQUEST_POST, _('POST')),
        (REQUEST_PARAM, _('PARAM')),
)
