#!/usr/bin/env python

import json
import sqlite3
from bottle import route, run, template


#----------------------------------------------------------------------------------------------

def test123():
	global sum, get_c, url_c, post_c, query3_c, status_code
	sum = 0
	get_c = 0
	url_c = 0
	post_c = 0
	query3_c = 0
	list_data = []
	status_code = {}
	print 'success'

	txt = open("./apsc_2015-10-30.log", 'r')
	for i in  txt.readlines():
		try:
			#list_data.append(i)

			if 'GET' in i:
				get_c += 1
			elif  'POST'  in i:
				post_c +=1
				if '/query3'  in i:
					query3_c += 1
	
			if 'GET' or 'POST'  in i.split()[5]:
				url_c += 1

			if i.split()[8] not in status_code:
				status_code[i.split()[8]] = 1
			else:
				status_code[i.split()[8]] += 1
			sum += int(i.split()[9])
		except Exception as e:
			print 'Warning : %s' % e
	txt.close()
	#print 'total = %s'  % len(list_data)
	print '-' * 30
	print 'GET_count = %s'  % get_c
	print 'POST_count = %s' % post_c
	print 'query3_count = %s' % query3_c
	print 'url_count = %s' % url_c
	print '-' * 30
	print 'status_code:'
	global total
	total = {}
	total['GET'] = get_c
	total['POST'] = post_c
	total['query3'] = query3_c
	total['URL'] = url_c

	for j in status_code:
		print '%s = %s' % (j, status_code[j])

	print '-' * 30
	print 'average = %sB' % (sum / url_c)
#-------------------------------------------------------------------

def insert_database():
	conn = sqlite3.connect('test.db')
	print "Opened database successfully";
	cur = conn.cursor()
	#sql = 'create database test123; use test123; create table info values(id int(20), name char(20);'
	flag = 1
	for z in total:
		print z
		print total[z]
		sql = "insert into test123 values(%d, '%s', %d)" % (flag, z, total[z])
		cur.execute(sql)
		flag += 1
	cur.close()
	conn.commit()
	conn.close()

#------------------------------------------------------------------
if  __name__ == '__main__':
	test123()
	#@route('/query/<name>')
	#def index(name):
	#    return template('<b>Hello {{name}}</b>!',name=name)
	insert_database()
	@route("/query")
	def login():
		return '<b> url_count = %s </b><br><b> GET_count = %s </b><br> \
			<b> POST_count = %s </b><br><b>query3_count = %s </b><br>\
			<b> status_code = %s</b><br>'   %  (url_c, get_c, post_c, query3_c, status_code)
	run(host='10.255.40.245', port=8080)
