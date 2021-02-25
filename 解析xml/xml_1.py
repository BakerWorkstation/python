#import  xml.dom.minidom
#dom = xml.dom.minidom.parse('c:\\Users\\admin\\Desktop\\4F843D0715C6DEC6D9EF60C3DF50BF37.E786A083.avml')
#root = dom.documentElement
##b = root.getElementsByTagName('SCANNER')
#print b[0].getAttribute('name')

from xml.etree import ElementTree as ET

per = ET.parse('c:\\Users\\admin\\Desktop\\C01A37FCB586AA3B73B89DABE9B7401A.62A2D04B.avml')
per = per.getroot()
#a = per.getElementsByTagName('SCANNER')
#print a[0].firstChild.data
#for i in a:
#	try:
#   	 print i
#		 print i.firstChild.data
#	except Exception as e:
#		 print str(e)
#		 pass

o = per.findall('./PROC/HASH')
for k in range(len(o)):
	for child in o[k].getchildren():
		print child.tag,":",child.text

print  '-'*35
p = per.findall('./SCAN/FILESIZE')
for j in range(len(p)):
	print p[j].tag, ':', int(round(float(p[j].text)/1024)), 'KB'


q = per.findall('./SCAN/SCANNER')
for i in range(len(q)):
	print  '-'*35 
	print q[i].tag, ':', q[i].get('name')
	for child in q[i].getchildren():
		print child.tag,":",child.text
	