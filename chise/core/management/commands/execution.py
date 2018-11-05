# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from chise.core.backends.execution import ExecutionBackend
from chise.core.tasks import execution_task

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        pass

    def add_arguments(self, parser):
        parser.add_argument("-id", dest="execution_id")
        parser.add_argument("-delay", dest="delay", default=1)

    def handle(self, *args, **options):
        try:
            execution_id = options['execution_id']

            if int(options['delay']) == 0:
                execution_task(execution_id)
            else:
                execution_task.delay(execution_id)

        except CommandError:
            pass

       
