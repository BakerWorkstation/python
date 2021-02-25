from urllib.parse import quote

IP = "10.255.175.109"
PORT = "6379"
MISSION = "13"
RESULT = "12"
PASSWORD = "antiy?pmc"

PASSWORD = quote(PASSWORD)

BROKER_URL = 'redis://:{}@{}:{}/{}'.format(PASSWORD, IP, PORT, MISSION) # 使用Redis作为消息代理

CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/{}'.format(PASSWORD, IP, PORT, RESULT) # 把任务结果存在了Redis

CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案
# CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # celery任务结果有效期

CELERY_ACCEPT_CONTENT = ['json', 'msgpack'] # 指定接受的内容类型

CELERY_TIMEZONE = 'Asia/Shanghai' # celery使用的时区
CELERY_ENABLE_UTC = True # 启动时区设置
CELERYD_LOG_FILE = "/var/log/celery/celery.log" # celery日志存储位置

CELERYD_CONCURRENCY = 1  # 并发worker数
# CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行100个任务就会被销毁