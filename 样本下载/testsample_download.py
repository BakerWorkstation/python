#!/usr/bin/env python
import os
import sys
import urllib2
from datetime import datetime

date = datetime.now().strftime("%Y%m%d")
localdir = "/opt/gx/to_yiyan/" + date + "/"

download_addr = ['http://172.16.1.153:80/download/',
                 'http://172.16.1.153:82/download/', 
                 'http://172.16.1.159:80/download/',
                 'http://172.16.1.159:82/download/',
                 'http://172.16.1.110/download/',
                 'http://172.16.1.110:82/download/',
                 'http://172.16.1.110:83/download/']


def  handle_list():
    sample_list = []
    if 'virustotal.txt'  in os.listdir(localdir):
        sample_file = localdir + "virustotal.txt"
        for readline in open(sample_file, 'r'):
            sample_list.append(readline.split()[0].strip())
    else:
        print 'Warning : "virustotal.txt" not found in %s' %  date
        os._exit(0)
    return  sample_list


def judge_sample_exist():
    os.system('python /opt/gx/to_yiyan/do_query.py')
    counter = 0
    success = []
    down_list = handle_list()
    for md5 in down_list:
        for readline in download_addr:
            try:
                url = readline + md5
                string = urllib2.urlopen(url)
                data = string.readline()
                if  data :
                    flag = 'True'
                    break
            except Exception as e:
                flag = 'False'
        if flag == 'True':
            counter +=1
            success.append(md5)
            if  counter == 1000:
                f = open(localdir + '1.txt' ,'w')
                for i in success:
                    f.write(i+'\n')
                f.close()
                command = 'scp %s1.txt 10.255.49.42:/opt/sdc/%s/list/' % (localdir, date)
                os.system(command)
                command1 = 'scp %ssource_repeat.txt 10.255.49.42:/opt/sdc/%s/list/' % (localdir, date)
                os.system(command1)
                command2 = 'scp %ssource_total.txt 10.255.49.42:/opt/sdc/%s/list/' % (localdir, date)
                os.system(command2)
                break


def Friday():
    os.chdir('/opt/gx/to_yiyan')
    sample_list = []
    success = []
    num = int(datetime.now().strftime('%Y%m%d'))
    for j in range(0,5):
        day = num - j
        if os.path.exists(str(day)):
            for z in os.listdir(str(day)):
                if z in ('kingsoft_4w.txt', 'kingsoft.txt', 'huawei.txt', 'vds.txt'):
                    txt = open('%s/%s' % (day, z), 'r')
	            for x in txt.readlines():
                        sample_list.append(x.split()[0].strip())
                    txt.close()
    temp = len(sample_list)
    txt_vt = open('%s/virustotal.txt' % str(num), 'r')
    for v in txt_vt.readlines():
        sample_list.append(v.split()[0].strip())
    txt_vt.close()
    print len(sample_list)
    for b in sample_list:
        for n in download_addr:
            url = n+b
            try:
                if urllib2.urlopen(url).readline():
                    success.append(b)
                    print len(success)
                    if  len(success) == 2000:
                        #ff = open('./11.txt', 'w')
                        #for m in success[ 2000-temp-1 : 2000]:
                        #    ff.write('m'+'\n')
                        #ff.close()
                        for m in success:
                            print m
                        break
            except Exception as e:
                print e 
    
                    
if __name__  == '__main__' :
    os.system('clear')
    if not sys.argv[1]  == 'Fri':
        judge_sample_exist()
    else:
        Friday()
