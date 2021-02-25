'''
@Author: sdc
@Date: 2020-06-22 13:37:55
@LastEditTime: 2020-06-28 14:06:50
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/56/except/pull_data.py
'''

#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-
# __author__: sdc

import time
import threading
import confluent_kafka
from timeWindow import *
from multiprocessing import Process
from confluent_kafka import Consumer, KafkaError, TopicPartition


'''
@description: 通过网络侧数据，检测敏感文件被下载
@param {type} 
@return: 
'''
def downloadFile(log):
    logData = json.loads(log)
    # 旧版标准化日志
    print('日志ID -> %s' % logData["hbase_rowkey"])
    print('源IP -> %s' % logData["threat_info"]["source_endpoint"]["ip_info"]["ip"])
    print('目的载荷文件名 -> %s' % logData["threat_info"]["purpose_load"]["o_filename"])
    for eachsource in logData["threat_info"]["source_load"]:
        print('源载荷文件名 -> %s' % eachsource["o_filename"])
    print('-' * 50)
    return 'sucess', ''


'''
@description:    kafka消费者处理数据函数
@param {type}    topic(string),  partition(int),  functions(object),  redis_conn(object)
@return:
'''
def consumeData(topic, partition, functions, redis_conn):
    offsetkey = "%s_%s" % (topic, partition)
    redis_offset = redis_conn.get(offsetkey)
    broker_list = "%s:%s" % (kafka_ip, kafka_port)
    producer = confluent_kafka.Producer({"bootstrap.servers": broker_list})
    tp_c = TopicPartition(topic, partition, 0)
    consume = Consumer({
                        'bootstrap.servers': broker_list,
                        'group.id': group_id,
                        'enable.auto.commit': False,
                        'max.poll.interval.ms': max_poll,
                        'default.topic.config': {'auto.offset.reset': reset}
    })
    # 获取数据对应最小offset 与 redis记录中的offset比较
    kafka_offset = consume.get_watermark_offsets(tp_c)[0]
    if not redis_offset:
        offset = kafka_offset
    else:
        if int(redis_offset) > kafka_offset:
            offset = int(redis_offset)
        else:
            offset = kafka_offset
    # 重新绑定offset 消费
    tp_c = TopicPartition(topic, partition, offset)
    consume.assign([tp_c])
    data = consume.consume(length, timeout)
    write_offset = offset
    if data:
        #print("topic: %s  partition: %s\t  data_length : %s" % (topic, partition, len(data)))
        for eachmsg in data:
            if eachmsg.error():
                print('error: %s' % eachmsg.error())
                write_offset += 1
                continue

            
            # 处理日志数据函数  flag: 'parse'(消息解析错误)/'error'(消息处理失败)/'success'(消息处理成功)
            flag, message = functions[topic](eachmsg.value())
            flag = ''
            write_offset += 1
            # 数据解析失败，需要往新话题写入数据
            if flag == 'parse':
                print(message)
                #producer.produce('parse_error', eachmsg.value())
                #producer.flush(timeout=1) #  0: 成功  1: 失败
            # 数据处理失败，需要往原话题写回数据
            elif flag == 'error':
                print(message)
                #producer.produce(topic, eachmsg.value())
                #producer.flush(timeout=1) #  0: 成功  1: 失败
            # 数据处理成功
            else:
                pass
            # with main_thread_lock:
            #     pass
    else:
        print("topic: %s  partition: %s\t无数据" % (topic, partition))
    # 处理结束后， redis中更新offset
    tp_c = TopicPartition(topic, partition, write_offset)
    # 获取当前分区偏移量
    kafka_offset = consume.position([tp_c])[0].offset
    # 当前分区有消费的数据, 存在偏移量
    if kafka_offset >= 0:
        # 当redis维护的offset发成超限时，重置offset
        if write_offset > kafka_offset:
            write_offset = kafka_offset
    redis_conn.set(offsetkey, write_offset)
    consume.commit(offsets=[tp_c])


'''
@description:    kafka阻塞式消费数据
@param {type}    topic(string),  partition(int),  functions(object),  redis_conn(object)
@return:
'''
def reset_offset(topic, partition, functions, redis_conn):
    while True:
        try:
            consumeData(topic, partition, functions, redis_conn)
            time.sleep(3)
        except Exception as e:
            print("Error: consumeData function -> message: %s" % str(e))
            continue


'''
@description:  单个进程启动多线程，一个线程对应一个kafka分区 消费
@param {type}  topic(string), functions(object)
@return: 
'''
def handle(topic, functions):
    redis_conn = redis_connect()
    threads = []
    for partition in range(partitions):
        child_thread = threading.Thread(
                                        target=reset_offset,
                                        args=(
                                                topic,
                                                partition,
                                                functions,
                                                redis_conn,
                                        ),
                                        name='LoopThread'
        )
        threads.append(child_thread)
    for eachthread in threads:
        eachthread.start()
    for eachthread in threads:
        eachthread.join()


'''
@description:  主函数
@param {type} 
@return: 
'''
def main():
    processes = []
    functions = {
        "Standardization_WhiteData": downloadFile
    }
    topics = ["Standardization_WhiteData"]
    for eachtopic in topics:
        p = Process(target=handle, args=(eachtopic, functions, ))
        print('Child process will start.')
        processes.append(p)
    for eachprocess in processes:
        eachprocess.start()
    for eachprocess in processes:
        eachprocess.join()


if __name__ == "__main__":
    main()
