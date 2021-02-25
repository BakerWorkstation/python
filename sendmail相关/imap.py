#!/usr/bin/env python

from imaplib import IMAP4

i = IMAP4('imap.server.com',143)
i.login('test', '000000')
inbox = i.select('INBOX')
type, data1 = i.search(None, 'all')
dat = data1[0].split()
ff = open('./imap.mail','w')
for data_new in dat:
	print data_new
	type,data_new = i.fetch(data_new,'RFC822')
	data = data_new[0][1].replace('\r','')
	ff.write(data)
ff.close()
i.close()
