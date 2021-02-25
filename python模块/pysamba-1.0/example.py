#!/usr/bin/env python
##############################################################################
##
## example.py
##
## Created: 04/12/07 08:04:36
## Author: Juan M. Casillas <juanm.casillas@jmcresearch.com>
##
## a simple example to exercise pysamba module
##
## $Header$
##
## $Log$
##
##############################################################################

#
# test my module
#
  
if __name__ == "__main__":

  from pysamba import SMBManager

  host="smbserver"
  share="myshare"
  user="myuser"
  passwd="mysecret"
  domain="MYDOMAIN"

  svr = SMBManager(host,share,user,passwd,domain)
  if not svr.Connect():
    print "Can't connect with server"
    sys.exit(1)

  print svr.DiskAvail()            
  print svr.DirSize("\\onedir")    
  svr.GetDir("\\onedir", "/tmp")   
  svr.Mkdir("\\backups\\src", True)
  svr.PutDir("/usr/tmp/samba-3.0.24","\\backups\\src")
  svr.Rmdir("\\crappydir",True)

  svr.Chdir("\\onedir\\listmedir")
  print svr.Pwd()
  svr.PrettyList()

  svr.GetFile("\\onedir\\remote.png","/tmp/local.png")
  svr.PutFile("/tmp/local2.png","\\onedir\\remote2.png")  

