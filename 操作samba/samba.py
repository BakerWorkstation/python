#import urllib2
#from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection
#import smbclient

conn = SMBConnection("Burning", "123///", "tabsang", "localhost", use_ntlm_v2 = True)

conn.connect("172.16.",139)

print conn.listShares()
print len(conn.listPath("share","/150/20160130/bin/"))
f = open("E:/1.txt","w")
file_attributes, filesize = conn.retrieveFile("share","/150/20160130/bin/clusterdb",f)
f.close()
conn.close()