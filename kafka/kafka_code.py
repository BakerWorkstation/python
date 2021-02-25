#!/usr/bin/env python
# coding=utf-8
import os
import sys,json
import time
import datetime
import random
import threading
import time
from confluent_kafka import Consumer, KafkaError, Producer, KafkaException, TopicPartition, Message, admin

#写生产者接口
#写消费者接口
#写处理数据接口
#写数据库调用接口


#生产者 消费者 （生产数据和消费数据测试）
#生产者 消费者 （尝试修改配置{分区 消费者数 同步分区设置} 输出配置）
#生产者 消费者 （测试压缩与不压缩 效率 数据大小等）
#生产者 消费者 （测试同步异步的效率等 差别）
#生产者 消费者 （可靠性测试）
#kafka的运维（修改话题配置 添加删减分区 ）
#生产者 消费者的操作 
#admin操作测试



    
    
    
def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))#输出错误信息
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))#输出错误消息发送向哪个分区 话题





def Producer_history(topics,data):      #生产者
    object = Producer({"bootstrap.servers":"10.255.52.3:9092"})# 连接kafka
    object.produce(topics,data.encode("utf-8"),callback=delivery_report)
    c=object.flush()
    return c

def Cunsumer_history(group_id,topics,partition_id,read_len): #消费者
    conf={'bootstrap.servers':'10.255.52.3:9092','group.id':group_id,'session.timeout.ms':'6000','default.topic.config':{'auto.offset.reset':'smallest'}}
    object = Consumer(conf)
    #object.subscribe(topics)
    partition_id=0 if partition_id==None else partition_id
    B=TopicPartition(topic=topics[0],partition=partition_id)
    object.assign([B])
    for i in range(read_len):
        try:
            ms=object.consume(1,2.0)
            msg=ms[0]
            print msg.__len__()
            print msg.headers()
            print msg.key()
            print msg.offset()
            print msg.partition()
            print msg.timestamp()  #(1, 1533274980035L)输出格式
            print msg.topic()
            print msg.value()
        except Exception as e:
            print ("Failed to read topic {}: {}".format(topics[0], e))
#["opt_info","deal_info","network_info","device_info"]
def create_topic(topics): #创建话题
    object=admin.AdminClient({"bootstrap.servers":"10.255.52.3:9092"})
    new_topics = [admin.NewTopic(topic, num_partitions=4, replication_factor=1) for topic in topics]
    fs = object.create_topics(new_topics)
    print fs
    for topic, f in fs.items():
        print f
        try:
            f.result()  # The result itself is None  失败会跳出到except
            print f.result(),"hehe"
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
def producer_1(begin,number):#测试producer功能
    #Producer(config)
    #__len__()  与文档写的不一样 没有了len()方法
    #flush(timeout)   开始发一堆消息 发出一个队列的g:Message delivered to my1 [0]这种消息 然后 好像回一个NONE   成功写入到话题中时会收到一堆eg：Message delivered to my1 [0]
    #list_topic(topic timeout)
    #poll(timeout)  poll传递消息是会发出eg:Message delivered to my1 [0]这种消息 表示发出了一条消息 发向哪个话题哪个分区成功 写入到话题中时会收到eg：Message delivered to my1 [0]
    #produce(topic value key partition callback partition timestamp headers)
    print 3
    object = Producer({"bootstrap.servers":"10.255.52.3:9092"})
    a=[]
    print 1
    for i in range(500):
        a.append("aaaaaan"+str(i))
    a1=time.time()
    print object.__len__()
    for data in a:
        #msg=object.poll(0)#轮询生产者的事件并调用相应的回调（如果已注册）。生产者也有轮询poll？ 使上一条缓存中的数据发送出去 并在发送出去之前阻塞其他请求 请求完成标准是 (轮询好像就是发送请求 看有没有把数据读出来 或则插进去 )
        #之前acks的同步分区都写入了是成功 否则返回错误。其他线程可以继续发送消息，同时阻塞一个线程等待刷新调用完成;但是，不保证在刷新呼叫开始后发送的消息完成
        object.produce("my1",data.encode("utf-8"),"5ey2",callback=delivery_report)
    #for data1 in a:
    #    #轮询生产者的事件并调用相应的回调（如果已注册） 。生产者也有轮询poll？ 使上一条缓存中的数据发送出去 并在发送出去之前阻塞其他请求 请求完成标准是
    #    #之前acks的同步分区都写入了是成功 否则返回错误。其他线程可以继续发送消息，同时阻塞一个线程等待刷新调用完成;但是，不保证在刷新呼叫开始后发送的消息完成
    #    object.produce("my1",data1.encode("utf-8"),"key1",callback=delivery_report)
    ##time.sleep(2)
    
    print object.__len__()
    b=object.list_topics("my1",1.0)
    print 2
    print b.cluster_id
    print b.brokers
    print b.topics
    print b.controller_id
    c=object.flush()
    print c  #输出有多少个还在队列里没发出去
    print time.time(),a1
    

def Consumer_1(begin,number): #测试消费者功能
    conf={'bootstrap.servers':'10.255.52.3:9092','group.id':'group11','session.timeout.ms':'6000','default.topic.config':{'auto.offset.reset':'smallest'}}
    object = Consumer(conf)
   # object.subscribe(["my1"])
    x=True
    k=1
    print "begin"
    B=TopicPartition(topic="my1",partition=0,offset=158)
    B1=TopicPartition(topic="my1",partition=1,offset=2)
    C=TopicPartition(topic="my1",partition=0)
    E=TopicPartition(topic="my1",partition=1)
  #  object.seek(B) #找不到分区 不知道为啥 报val=-190 (因为没有assign)  不好使 是因为不兼容1.1？？
    object.assign([B])  #自定位offset assign后面跟着poll 或consumer 好使 中间隔开不好使 为啥？ 找到原因了 我日 subscribe 不能跟assign同时使用 
   # object.seek(E)
   # print object.offsets_for_times([E])
    topic_object=admin.NewTopic("file_name",4,replication_factor=1)
    print "end"
    try:
        while x:
            k+=1
          #  object.assign([B])
           # msg=object.poll(1.0)  #(一个一个读取  参数是超时时间 )
            ms=object.consume(1,2.0)         #consume  读的是从leader分区读
            print ms
            msg=ms[0]
            if msg is None:
                print "haha"
                continue  #读不存在的topic  返回
                            # -191
                            # _PARTITION_EOF
                            # Broker: No more messages
                            # haha

            if msg.error():
                print msg.error().code()
                print msg.error().name()
                print msg.error().str()
            else:
                print "hehe ",msg
          #      object.resume([C,E])            #  取消消费选leader 要不没用
                print msg.__len__()
                print msg.headers()
                print msg.key()
                print msg.offset()
                print msg.partition()
                print msg.timestamp()  #(1, 1533274980035L)输出格式
                print msg.topic()
                print msg.value()
                print object.position([C]) #返回值：[TopicPartition{topic=my51,partition=0,offset=92,error=None}]  有bug 得到-1001 好像是因为分片里没数据
            if k == 10:
                x=False
                print "***********************"
                print object.get_watermark_offsets(C) #eg  (0L, 510L)
                print object.list_topics("my1")  #返回ClusterMetadata类对象
                print object.assignment()  #返回值：[TopicPartition{topic=my1,partition=0,offset=-1001,error=None}] 可能是因为没有用assign分配过 几个分片返回几个
                print topic_object
    except Exception as ex:
        return str(ex)
  #  object.resume([C])
    time.sleep(2.0)
    object.close()
    time.sleep(5.0)
    return 0





# def product(begin,number):
    # object=open("/home/kafka_2.11-1.1.0/test.txt","ab+")
    # print "文件名: ", object.name
    # for i in range(number):
        # k=begin+i
        # object.write(str(k)+"iimportadsfawefasdfasdfasdfasdfafthreading"+str(k)+"\n") 

    
if __name__=="__main__":
    print "aaaaaan"
    #print producer_1(1,2)
    print "aa"
    
    #print Consumer_1(1,2)
    #create_topic(["opt_info","deal_info","network_info","device_info"])
    data={
    "OS":"操作系统",
    "IPMAC":"终端ipmac",
    "Version":"系统版本",
    "uuid":"客户端uuid",
    "device_opt":[    #外设操作
                    {
                        "device_id":"外设pid",
                        "process_action":"操作动作",
                        "opt_process_path":"操作进程路径",
                        "opt_process_md5":"操作进程md5",
                        "opt_file_path":"被操作文件路径",
                        "opt_file_md5":"被操作文件MD5",
                        "action_time":"操作时间"
                    }
                    ],
    "device_info":[ #外设信息
                    {
                        "device_id":"外设pid",
                        "device_name":"外设名称",
                        "statue":"接入状态",
                        "type":"外设类型",
                        "action_time":"操作时间"
                    }
    ]
    }
    data=json.dumps(data)
    Producer_history("device_info",data)
    Cunsumer_history("group_id",["device_info"],3,1)