'''
@Author: sdc
@Date: 2020-03-23 13:47:50
@LastEditTime: 2020-06-10 14:25:16
@LastEditors: Please set LastEditors
@Description: 创建表结构
@FilePath: /opt/createTabel.py
'''

#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-
# __author__: sdc


from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, String, Integer, Text, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

# # 定义原始日志对象:
# class h_originlog_info(Base):
#     # 表的名字:
#     __tablename__ = 'h_originlog_info'

#     # 表的结构:
#     id = Column(Integer , primary_key=True, autoincrement=True)
#     message = Column(Text)
#     rtime = Column(Integer)


# # 定义日志跟标签对应对象:
# class h_loglabel_info(Base):
#     # 表的名字:
#     __tablename__ = 'h_loglabel_info'

#     # 表的结构:
#     id = Column(Integer , primary_key=True, autoincrement=True)
#     logid = Column(Text)
#     labelname = Column(String(128))
#     chinesename = Column(String(128))
#     event = Column(Text)
#     rtime = Column(Integer)

# # 定义日志跟标签对应对象:
# class h_whitelist_info(Base):
#     # 表的名字:
#     __tablename__ = 'h_whitelist_info'

#     # 表的结构:
#     id = Column(Integer , primary_key=True, autoincrement=True)
#     md5 = Column(String(32))
#     url = Column(Text)
#     rtime = Column(Integer)

# #   设备模板格式表
# class h_device_info(Base):
#     __tablename__ = 'h_deviceformat_info1'
#     mid = Column(String(32), primary_key=True)
#     dname = Column(String(64), comment="设备名称")
#     example = Column(Text, comment="设备数据格式")
#     key = Column(postgresql.ARRAY(String), comment="最外层key列表集合")

class abc(Base):
    __tablename__ = 'abc'
    mid = Column(String(32), primary_key=True)
    key = Column(postgresql.ARRAY(String), comment="最外层key列表集合")

# #   设备模板映射表
# class h_map_info(Base):
#     __tablename__ = 'h_devicemap_info1'
#     id = Column(Integer , primary_key=True, autoincrement=True)
#     mid = Column(String(32), ForeignKey("h_deviceformat_info1.mid"))
#     dfield = Column(Text, comment="设备字段")
#     mfield = Column(Text, comment="标准化字段")


# 初始化数据库连接:
#engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
engine = create_engine('postgresql+psycopg2://postgres:postgresql_superuser@10.255.:5432/gogogo')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)