# -*- coding: utf-8 -*-
###################################################################################################
#                                      FILE INFOMATION                                            #
#                  ========================================================                       #
#                  Creater	:  shenchangwei  <changwei_shen@antiy.com>                    	      #
#                  Create Time  :  2014-08-28    11:00:00                                         #
#                  Company      :  Antiy Labs    (Harbin, China)                                  #
#                  Location     :  Harbin, China                                                  #
#                                                                                                 #
#                                      LEGAL                                                      #
#                  ========================================================                       #
#                  Copyright (C) Antiy Labs. All right reserved.                                  #
#                                                                                                 #
#                                      FILE DESCRIPTION                                           #
#                  ========================================================                       #
#                   download sample                                                               #
#				                                                                                  #
###################################################################################################

import os, sys
import urllib2
import logging

#下载样本地址
URL_DOWNLOAD_LIST = ['http://172.16.1.187:9090/download/']

def download_main(list_hash, sample_save_dir):
	'''
	下载主程序
	参数
		list_hash    		包含文件散列(md5.crc32)
		sample_save_dir	    样本存储目录
	
	返回值 无
	'''
	
	if (not os.path.lexists(sample_save_dir)):
		os.makedirs(sample_save_dir)
	i=0
	fail = 0
	for hash in list_hash:
		print hash	
		sample_full_path = os.path.join(sample_save_dir, hash)
		flag = False
		buf = None
		for u in URL_DOWNLOAD_LIST:
			url = '%s%s'%(u,hash.strip())
			try:
				print url		
				h = urllib2.urlopen(url, timeout=30)
				buf = h.read()
				h.close()
				#if buf == '{\n\t"X-Operate-Message": "Error: master file does not exist!",\n\t"X-Operate-Status": "FAILURE"\n}':
				if 'FAILURE'  in buf:
					f=open('fail.txt','ab')
					f.write('[ERROR] Download %s error\n' % hash.strip())
					f.close()
					continue
				flag = True
				break
			except Exception, e:
				if str(e).find('Not Found') == -1:
					print '[ERROR] Download %s error(%s)'%(hash.strip(), str(e).strip())
				continue
				
		if (not flag):
			fail = fail + 1
			print '[INFO] Not Found %s'%(hash.strip())
			print '下载失败有%s个样本\n' %(fail)
			continue
			
		try:
			with open(sample_full_path, 'wb') as fp:
				fp.write(buf)
			i = i + 1
			print hash
			print "已成功下载%s个样本\n" % i
		except Exception, e:
			print str(e).strip()
							
	return
	

if __name__ == "__main__":
	'''
	基于样本散列文件列表下载样本
	参数1:  样本散列文件 支持格式：
			(1) MD5.crc32
			(2) MD5\tcrc32
	参数2: 样本保存目录
	'''	
	
	sample_path = sys.argv[2]
	
	list_hash = []
	for ele in open(sys.argv[1], 'rb'):
		info = ele.replace("'", '').replace('"', '').strip()#.upper()
		list_hash.append('%s.%s'%(info[:32], info[33:].strip()))
	download_main(list_hash, sample_path)

