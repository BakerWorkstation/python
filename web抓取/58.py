#! -*- coding:utf-8 -*-

import urllib2

name = []
url = []
z = -1
list1 = []
data1 = urllib2.urlopen('http://hrb.58.com/zhuangxiugs/pn1').readlines()
for i in data1:
	z += 1
	list1.append(i)
	if  '<a href' and 'clickLog' in i:
		if i[-3] == 'a':
			#if '公司' in i :
			url_data = list1[z-6].split("onclick")[0].split('href=')[-1].replace('"','').replace("'",'').split(' target')[0].strip()
			if 'http' in url_data:
				url.append(url_data)
			else:
				continue
			#if z/6 == 0:
			name_data = list1[z].split('</a>')[0].split('>')[-1].split('次')[0]#.split("onclick")[0].split('href=')[-1].replace('"','').replace("'",'').strip()
			if name_data:
				name.append(name_data)

a=0
b=0
for i in range(0,len(url)):
#for i in range(0,1):
	#print url[i]
	print i
	print '-'*100
	print url[i]
	#print url[i]
	print name[i]
	data2 = urllib2.urlopen(url[i]).readlines()
	list2 = []
	j = 0
	for i in data2:
		list2.append(i)
		if '<span class="l_phone">' in i:
			a = j
			pass
		if '>详细地址' in i:
			b = j + 1
		j += 1

	print '电话 :', list2[a].split('<em>')[0].split('>')[-1].strip()
	print '地址 :', list2[b].split('-')[-1].strip()
