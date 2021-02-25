#!/usr/bin/python
# -*- coding:UTF-8 -*-

from sshtunnel import SSHTunnelForwarder

class T(object):
    
    def __init__(self):
        __self.api1   =  ('10.10.10.80', '15170')    # api1
        __self.api2   =  ('10.10.10.77', '15171')    # api2
        __self.task1  =  ('10.10.10.78', '15172')    # task1
        __self.task2  =  ('10.10.10.74', '15173')    # task2
        __self.web1   =  ('10.10.10.70', '15174')    # web1
        __self.web2   =  ('10.10.10.69', '15175')    # web2
        __self.web3   =  ('10.10.10.92', '15176')    # web3
       
    def webTunnel(self):
        self.webServer = SSHTunnelForwarder(
                                            ssh_address_or_host=('47.75.66.217', 60022),
                                            ssh_username="13504845624",
                                            ssh_password="Baker@231",

                                            remote_bind_addresses=[
                                                                   (__self.web1[0], 15170),
                                                                   (__self.web2[0], 15170),
                                                                   (__self.web3[0], 15170)],
                                            local_bind_addresses=[
                                                                  ('127.0.0.1', __self.web1[-1]),   #  web1
                                                                  ('127.0.0.1', __self.web2[-1]),   #  web2
                                                                  ('127.0.0.1', __self.web3[-1])]   #  web3
                                           )
            
    def apiTunnel(self):
        self.apiServer = SSHTunnelForwarder(
                                            ssh_address_or_host=('47.75.66.217', 60022),
                                            ssh_username="13504845624",
                                            ssh_password="Baker@231",

                                            remote_bind_addresses=[
                                                                   (__self.api1[0], 15170),
                                                                   (__self.api2[0], 15170)],
                                            local_bind_addresses=[
                                                                  ('127.0.0.1', __self.api1[-1]),   #  api1
                                                                  ('127.0.0.1', __self.api2[-1])]   #  api2
                                           )

    def taskTunnel(self):
        self.taskServer = SSHTunnelForwarder(
                                             ssh_address_or_host=('47.75.66.217', 60022),
                                             ssh_username="13504845624",
                                             ssh_password="Baker@231",

                                             remote_bind_addresses=[
                                                                    (__self.task1[0], 15170),
                                                                    (__self.task2[0], 15170)],
                                             local_bind_addresses=[
                                                                   ('127.0.0.1', __self.task1[-1]),   #  task1
                                                                   ('127.0.0.1', __self.task2[-1])]   #  task2
                                            )
