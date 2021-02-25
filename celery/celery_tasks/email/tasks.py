import time
import pysnooper
from celery_tasks.main import celery_app

from kombu import serialization
serialization.registry._decoders.pop("application/x-python-serialize")

celery_app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
)

@celery_app.task(name='seed_email') # 添加celery_app.task这个装饰器，指定该任务的任务名name='seed_email'
def seed(mail):
    # time.sleep(1)
    return "发送邮件 %s" % mail["to"]
