from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExecutionConfig(AppConfig):
    name = 'execution'
    verbose_name = _('Execution')
