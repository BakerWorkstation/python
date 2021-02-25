#!/usr/bin/env python

#
# function ---> NO1. login in Baidu cloudy_disk and download files.
#               NO2. gpg  decrypt
#
# Created by BurNing at 2015-12-30
#

import os
import sys
import gnupg
import Queue
import shutil
#import logging
import tarfile
import datetime
import threading
#from multiprocessing import Process  # child_process
from multiprocessing import Pool     # process pool

global queue
queue = Queue.Queue(maxsize = 20)
#-----------------------------------------------------------------------------#
# logging
#class StreamToLogger(object):
#   """
#   Fake file-like stream object that redirects writes to a logger instance.
#   """
#   def __init__(self, logger, log_level=logging.INFO):
#      self.logger = logger
#      self.log_level = log_level
#      self.linebuf = ''

 #  def write(self, buf):
 #     for line in buf.rstrip().splitlines():
 #        self.logger.log(self.log_level, line.rstrip())


#-----------------------------------------------------------------------------#
def extract_files(file):
    directory = file.split('.')[0]
    tar  = tarfile.open('./%s' % file, 'r|gz')
    tar.extractall(path = './')
    tar.close()
    
    os.remove(file)
    
    shutil.copy(
                'get_tcp_dns.sh',
                './%s/get_tcp_dns.sh' % directory
               )
    # all.txt
    list_all = []
    list_virusname = {}
    
    os.chdir('./%s/' % directory)
    #shutil.copytree('%s.pcap' % directory, 'PCAP1')
    os.rename('%s.pcap' % directory, 'PCAP1')
    count = len(os.listdir('PCAP1'))
    os.system('bash get_tcp_dns.sh')
    
    os.chdir('..')
    # all_pcap.list
    for i in open('/opt/shanshi/20150507_all.txt', 'r'):
        list_all.append(i.split('\t')[0])
    
    # new_pcap.list
    for j in os.listdir('%s/Network1' % directory):
        if j.split('.pcap')[0] in list_all:
            os.remove('%s/Network1/%s' % (directory, j))

    # virusname_dict
    virusname = directory + '/' + directory + '.hash_virusname.list'
    for k in open(virusname, 'r'):
         list_virusname[k.strip().split(' |')[0]] = k.strip().split('| ')[-1]

    f = open('/opt/shanshi/20150507_all.txt', 'ab')
    for pcap in os.listdir('%s/Network1/' % directory):
        if pcap == None:
            break
        md5 = pcap.split('.pcap')[0]
        f.write(md5 + '\t' + list_virusname[md5] + '\n')
	os.rename(
                  '%s/Network1/%s' % (directory, pcap),
                  '/opt/shanshi/Network/%s' % pcap
                 )
    f.close()

    cha = 20 - len(file)
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ff = open('/opt/work/log.txt', 'ab')
    ff.write(today + '\t\t' + file + '\t' + str(count) + '\n')
    ff.close()
    return count
    #shutil.rmtree(directory)

#-----------------------------------------------------------------------------#
def list_files():   # Baidu_cloudy_disk api function
    global cmd_download, cmd_delete,file_list
    file_list = []

    #logging.basicConfig(
    #   level = logging.DEBUG,
    #   format = '%(asctime)s    %(levelname)s    %(name)s    %(message)s',
    #   filename = "out.log",
    #   filemode = 'a'
    #)

    # token every 30 days refresh
    token = '26.dca707f41721522578c5ec7f47d53f23.2592000.1464243045.1580463469-644561'

    cmd_list =     'curl -k -L\
                    "https://d.pcs.baidu.com/rest/2.0/pcs/file?method=list&\
                    access_token=' + token + '&path=/apps/bpcs_uploader/apps/"'

    cmd_download = 'wget -c --no-check-certificate -O %s\
                    "https://pcs.baidu.com/rest/2.0/pcs/file?method=download&\
                    access_token=' + token + '&path=/apps/bpcs_uploader/apps/%s"'

    cmd_delete =   'curl -k -L "https://d.pcs.baidu.com/rest/2.0/pcs/file?method=delete&\
                    access_token=' + token + '&path=/apps/bpcs_uploader/apps/%s"'

 
    whole = os.popen(cmd_list).read()
    whole = eval(whole)  # catch the list

    print whole
    for i in whole['list']:
        file = i['path'].split('/')[-1]
        file_list.append(file)
        queue.put(file)   
       
        #stdout_logger = logging.getLogger('download')
        #sl = StreamToLogger(stdout_logger, logging.INFO)
        #sys.stdout = sl
        
        #stderr_logger = logging.getLogger('STDERR')
        #sl = StreamToLogger(stderr_logger, logging.ERROR)
        #sys.stderr = sl
        #raise Exception('Test to standard error')

def download_files(file):
    try:
        os.system(cmd_download % (file, file))  # download file from Baidu cloudy disk
    except Exception as e:
        print 'Baidu_cloudy : ' , str(e)


#-----------------------------------------------------------------------------#
class TaskThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        filename = queue.get()

        # delete Baidu_cloudy disk file
        #os.system(cmd_delete % filename)

        gpg = gnupg.GPG(gnupghome = '/root/.gnupg')     # GPG decrypt
        privatekey = open('songdancheng.skr', 'rb')
        key_data = privatekey.read()
        privatekey.close()
        
        import_result = gpg.import_keys(key_data)
        private_keys = gpg.list_keys(True)
        
        pgpfile = open('%s' % filename, 'rb')
        pgpdata = pgpfile.read()
        pgpfile.close()

        if not filename[:-4] in os.listdir('./'): 
            gpg.decrypt(
                        pgpdata, 
                        passphrase = '',
                        output = '%s' % filename[:-4]
                       )
            #print decrypted_data
	    os.remove(filename)

            
#-----------------------------------------------------------------------------#
def  main():
    # total init
    global total
    total = 0
    os.chdir('/opt/work/')

    # download data
    list_files()
    if len(file_list) == 0:
        os._exit(0)

    # multi_child_proceess --> process pool
    pool = Pool(len(file_list))
    for i in file_list :
        pool.apply_async(
                         download_files, 
                         args=(i,)
                        )
	print 'start '
    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()

    # gpg decrypt
    while True:
        if queue.empty() :
            break
        th = TaskThread()
        th.setDaemon(True)
        th.start()
        th.join()
 
    # extract file
    for tar_file in file_list:
        tar_file = tar_file.split('.gpg')[0]
        count = extract_files(tar_file)
	total = total + count

    # total 
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ff = open('/opt/work/log.txt', 'ab')
    ff.write('%s\t\ttotal : %d\n' % (today, total))
    ff.close()

    # child_process
    #p = Process(target=run_proc, args=('test',))
    #print 'Process will start.'
    #p.start()
    #p.join()
 
if __name__ == '__main__':
    main()
