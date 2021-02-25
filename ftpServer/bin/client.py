'''
@Author: your name
@Date: 2020-04-29 15:31:31
@LastEditTime: 2020-04-29 15:34:14
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/ftpServer/bin/client.py
'''
# 搭建FTP客户端

from ftplib import FTP

import socket                # 主要用于获取当前主机IP地址

# 1. 实例化FTP对象, 并连接
ftp = FTP()
ftp.connect("10.255.175.185", 21)   # 应该输入服务器IP地址. 由于此处客户端与服务器建立在同一台主机上, 因此采用socket方法替代

# 2. 登录
ftp.login("ftpuser", "antiy?pmc")
# 匿名登录方法, 注意: 匿名用户的权限较低
# ftp.login("anonymous")

# 3. 交互
# 查看当前工作目录, 及指定目录下的内容
# print(ftp.pwd(), ftp.dir('./'))
# 下载文件
#ftp.retrbinary("RETR aaa.jpg", open("aaa.jpg", 'wb').write)
# 上传文件
ftp.storbinary("STOR 300m", open("300m", 'rb'))

# 4. 退出
ftp.quit()
