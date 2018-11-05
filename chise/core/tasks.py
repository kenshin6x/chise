# -*- coding: utf-8 -*-

from celery import shared_task
from chise.core.backends.execution import ExecutionBackend

@shared_task(default_retry_delay=2 * 60, max_retries=2)
def execution_task(execution_id):
    ExecutionBackend(execution_id).run()