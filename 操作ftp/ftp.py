import datetime
from ftplib import FTP
from os import system
from  shutil  import copytree

today = datetime.datetime.now().strftime("%Y%m%d")

copytree('D:/Japanese/Data','D:/'+today)
upload_file = 'D:/'+today+'.tar.gz'
system('E:\\WinRAR\\WinRAR.exe  a -k -r -s -m1 D:/%s.tar.gz  D:/%s' % (today,today))

connect = FTP("1.62.255.203")
connect.login("vsup", "xiaoxin2012up")
connect.cwd('mobile')
#data = []
#connect.dir(data.append)
f = open (upload_file,"rb")
connect.storbinary("STOR %s" % today+'.tar.gz',f,8192)
connect.quit()
f.close()
#for line in data:
#  print(line)

#os.chdir('C:/Users/Administrator/Desktop/')
#os.system('mkdir 1')

#csvfileList=common.WalkDir(csvfilepath+'csv_db/')
#for csvfileline in csvfileList:

