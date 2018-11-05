# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


STATUS_SUCCESS = 1
STATUS_FAIL = 2
STATUS_CHOICES = (
        (STATUS_SUCCESS, _('SUCCESS')),
        (STATUS_FAIL, _('FAIL')),
)


OBJECT_MODULE = 1
OBJECT_SCRIPT = 2
OBJECT_OTHER = 3
OBJECT_CHOICES = (
        (OBJECT_MODULE, _('MODULE')),
        (OBJECT_SCRIPT, _('SCRIPT')),
        (OBJECT_OTHER, _('OTHER')),
)


REFERENCE_START = 1
REFERENCE_END = 2
REFERENCE_RUNTIME = 3
REFERENCE_CHOICES = (
        (REFERENCE_START, _('START')),
        (REFERENCE_END, _('END')),
        (REFERENCE_RUNTIME, _('RUNTIME')),
)