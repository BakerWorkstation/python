'''
@Author: sdc
@Date: 2020-06-22 11:17:40
@LastEditTime: 2020-06-24 16:42:06
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/56/except/produceData.py
'''

import uuid
import random
from timeWindow import *
from clickhouse_driver import Client


# connect ClickHouse
client = Client(host="10.255.175.121", port=9000, user="default", database="funnel", password="antiy?pmc")

redis_conn = redis_connect()

def create(log):
    try:
        redis_conn.zadd("sensitiveData", {log: int(time.time())})
    except redis.exceptions.ConnectionError as e:
        print('redis生产数据失败 -> %s' % str(e))
        sys.exit(0)

    # 导入数据
    try:
        sql = "insert into sensitive (logid, ip, eventTime ,ltype) values('%s', '%s', %d, 1)" % (log, '10.255.175.%s' % random.randint(1, 254), int(time.time()), )
        print(sql)
        a = client.execute(sql)
        print(a)
    except Exception as e:
        print(str(e))
    

def cal():
    data = get_data(redis_conn)
    if len(data) >= count:
        print('True 大规模敏感数据泄露')

def main():
    while 1:
        log = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()))).replace("-", "").upper()
        create(log)
        
        cal()
        #time.sleep(0.1)


if __name__ == "__main__":
    main()