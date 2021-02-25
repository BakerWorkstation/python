__author__ = 'BurNing'
# -*- coding:utf-8 -*-
import os
import beanstalkc
import random
from pprint import pprint

beanstalk = beanstalkc.Connection(
                                    host = '10.255.40.195',
                                    port = 11301,
                                    parse_yaml = lambda x: x.split('\n')
                                    )

beanstalk.put(
                str(random.randint(1,100)),
                delay = 1,
                priority = 1024,
                ttr = DEFAULT_TTR
                )
while True:
    try:
        job = beanstalk.reserve(timeout=5)
        print job.body
        job.kick()
    except AttributeError as e:
        #os._exit(0)
        break
#job.delete()

print '-' * 50
print 'beanstalk.using : %s ' %  beanstalk.using()
print 'tubes : %s' % beanstalk.tubes()
print '-' * 20
beanstalk.use('test_001')
print 'beanstalk.using : %s ' %  beanstalk.using()
print 'tubes : %s' % beanstalk.tubes()
print '-' * 20

pprint(beanstalk.stats_tube('default'))
pprint(beanstalk.stats())

#job = beanstalk.peek(1)
job1 = beanstalk.peek_ready()
job2 = beanstalk.peek_delayed()
job3 = beanstalk.peek_buried()

#beanstalk.kick(10)

#server
#beanstalk.use('default')
#print 'beanstalk.using : %s ' %  beanstalk.using()
#print 'tubes : %s' % beanstalk.tubes()
#beanstalk.ignore('bar')

#client
#beanstalk.watch('default')
#print 'beanstalk.watching : %s ' %  beanstalk.watching()
#print 'tubes : %s' % beanstalk.tubes()
#beanstalk.ignore('bar')
beanstalk.close()

