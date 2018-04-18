from __future__ import absolute_import
from celery import Celery

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0', accept_content=['json'], include=['gather.tasks'])
