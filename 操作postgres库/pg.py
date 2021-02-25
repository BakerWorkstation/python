# -*- coding: utf-8 -*-

import psycopg2
import threading
import time

def  connect_pgdata() :
	cxn = psycopg2.connect(
                    host = '',
                    user = '',
                    password = '',
                    database = ''
                    )

	#data ='\'' + 'jerry' + '\''
	data='\'asdasd\''
	sql = "select * from  account where name = %s" % data
	cur = cxn.cursor()
	cur.execute(sql,data)

	rows = cur.fetchall()
	#cur.execute(sql)
	for i in rows:
		print i[0].strip()
	cur.close()
	cxn.commit()
	cxn.close()
def delay() :
	time.sleep(5)
	print 'finish_sleep'
if __name__ == '__main__':
	#T1 = threading.Thread(target=connect_pgdata())
	#T2 = threading.Thread(target=delay())
	#T2.start()
	#T1.start()
	connect_pgdata()
	#print 'finish'