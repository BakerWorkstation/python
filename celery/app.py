import time

from celery_tasks.email.tasks import seed

mission = seed.delay(dict(to='celery@python.org'))


print(mission)
while not mission.ready():
    print('sleep 1s')
    time.sleep(1)

print(mission.result)
