# UNTESTED
import urllib2
import sys
sys.path.append("E:/Python27/Lib/site-packages/smb/SMBConnection.py")
import smb
from smb.SMBConnection import SMBConnection

user_name = "root"
pass_word = "123///"
my_name = "anyname"
domain_name = ""
remote_smb_IP = "10.255.32.99"

conn = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2 = True)
assert conn.connect(remote_smb_IP , 139)

shareslist = conn.listShares()
for i in shareslist:
    print i.name
#with open('local_file', 'wb') as fp:
#    conn.retrieveFile(remote_smb_IP, '/iso/friday_report.txt', fp)
conn.close()
url = 'http://10.255.32.240/friday_report.txt'
print url
h = urllib2.urlopen(url, timeout=20)
buf = h.read()
print buf
h.close()
ff = open('local_file.txt', 'ab')
ff.write(buf)
ff.close
conn.close()
