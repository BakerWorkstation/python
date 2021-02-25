import datetime
import ftplib
import os
import shutil

today = datetime.datetime.now().strftime("%Y%m%d")

shutil.copytree('D:/Japanese/Data','D:/'+today)
upload_file = 'D:/'+today+'.tar.gz'
os.system('E:\\WinRAR\\WinRAR.exe  a -k -r -s -m1 D:/%s.tar.gz  D:/%s' % (today,today))


connect = ftplib.FTP("1.62.255.203")
connect.login("vsup", "xiaoxin2012up")
connect.cwd('mobile')
#data = []
#connect.dir(data.append)
f = open (upload_file,"rb")
connect.storbinary("STOR %s" % today+'.tar.gz',f,8192)
f.close()
connect.quit()

#for line in data:
#  print(line)

#os.chdir('C:/Users/Administrator/Desktop/')
#os.system('mkdir 1')

#csvfileList=common.WalkDir(csvfilepath+'csv_db/')
#for csvfileline in csvfileList:

