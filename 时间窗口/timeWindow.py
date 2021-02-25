'''
@Author: sdc
@Date: 2020-06-22 10:42:45
@LastEditTime: 2020-06-22 14:51:37
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/56/except/timeWindow.py
'''

#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-
# __author__: sdc

import os
import sys
import time
import json
import redis
import configparser

server_dir = '/opt/56/except/'

''' @description: 加载配置文件  '''
conf = configparser.ConfigParser()
conf.read(os.path.join(server_dir, "conf/server.conf"))
redis_passwd = conf.get("REDIS", "password").strip()
redis_ip = conf.get("REDIS", "ip").strip()
redis_port = int(conf.get("REDIS", "port"))
redis_db = int(conf.get("REDIS", "db"))
second = int(conf.get("WINDOW", "second"))
count = int(conf.get("WINDOW", "count"))

kafka_ip = conf.get("KAFKA", "ip").strip()
group_id = conf.get("KAFKA", "group_id").strip()
reset = conf.get("KAFKA", "reset").strip()
session_timeout = int(conf.get("KAFKA", "session_timeout"))
partitions = int(conf.get("KAFKA", "partitions"))
kafka_port = int(conf.get("KAFKA", "port"))
max_poll = int(conf.get("KAFKA", "max_poll"))
timeout = int(conf.get("KAFKA", "timeout"))
length = int(conf.get("KAFKA", "length"))

def redis_connect():
    # 开启redis连接池
    redis_pool = redis.ConnectionPool(
                                        host=redis_ip,
                                        port=redis_port,
                                        db=redis_db,
                                        password=redis_passwd,
                                        decode_responses=True
    )
    redis_conn = redis.Redis(connection_pool=redis_pool)
    return redis_conn

def get_data(redis_conn):
    # 从redis  gset中拉取数据
    try:
        data = redis_conn.zrangebyscore("sensitiveData", int(time.time())-second, int(time.time()), withscores=True)
    except redis.exceptions.ConnectionError as e:
        print('redis消费数据失败 -> %s' % str(e))
        sys.exit(0)

    return data
    
def main():
    redis_conn = redis_connect()
    get_data(redis_conn)

if __name__ == "__main__":
    main()