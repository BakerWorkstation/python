#!/usr/bin/env python
##############################################################################
##
## pysamba.py
##
## Created: 04/12/07 07:54:56
## Author: Juan M. Casillas <juanm.casillas@jmcresearch.com>
##
## Wraps the py_smb (smb) C extension module in order to provide high
## level operations, hidden the low-level module's complexity
##
## $Header$
##
## $Log$
##
##############################################################################

import sys
import os
import os.path
import re
import getopt
import glob

import smb        

class SMBManager:
  def __init__(self, host, res, user, passwd, domain):
      self.host   = host
      self.res    = res
      self.user   = user
      self.passwd = passwd
      self.dom    = domain

      self.IOSZ   = 8192
      self.bdf    = "/usr/bin/bdf"   # unix hardcoded :(

  def Connect(self):
      info_s = { 'domain': self.dom, 
                 'username': self.user,
                 'password': self.passwd
                 }
      
      try:
	smb.set_debuglevel(2)
	self.smb = smb.connect(self.host)
	self.smb.session_request(self.host)
	self.smb.negprot()
	self.smb.session_setup(info_s)
	self.smb.tconx(self.res)
      except Exception, e:
	print "Error: %s" % e
	return False

      return True

  def DiskAvailLocal(self,dir):
      "return the space available in bytes (totalb, availb, blocksize) (local)"

      if not os.path.exists(dir):
        return False
      
      cmd = "%s %s" % (self.bdf, dir)
      lines = self.GetCmdOutput(cmd)
      if len(lines) != 2: 
        return False

      size = lines[1].split()[3]
      return int(size)
      

  def DiskAvail(self):
      "return the space available in bytes"
      
      totalb,availb,bs = self.smb.diskavail()
      return bs * availb

  def List(self,dir):
      "list the given directory entries"
      
      return self.smb.list(dir)

  def ListRecursive(self,dirn=None, items=[]):
    "list recursively the given directory entries"

    litems = self.smb.list(dirn)
    newl = []

    for i in litems:

      p = i['name']

      if (i['isdir'] and i['name'] != "." and i['name'] != ".."):

        old = self.smb.pwd()

        self.smb.chdir(p)
        rec = self.ListRecursive()
        self.smb.chdir(old)

        for j in rec:

          if (j['isdir'] and (j['name'] == "." or j['name'] == "..")):
            continue

          if not j['name'].startswith('\\'): 
            j['name'] = "%s\%s\%s" % (old , i['name'] , j['name'])
          newl.append(j)

        if len(rec) == 0:
          #
          # insert the empty directory
          #
          newl.append(i)

      else:
        if i['name'] != '.' and i['name'] != '..':

          if len(self.smb.pwd()) > 1:
            i['name'] = "%s\%s" % (self.smb.pwd(), i['name'])
          newl.append(i)

    #
    # normalize paths
    #

    for i in newl:
      w = re.sub("[\\\\]+","$",i['name'])
      i['name'] = w.replace("$","\\")
    
    return newl


  def DirSize(self, dirn=None):
    "calculates the space occupied by dir"

    tsize = 0
    l = self.ListRecursive(dirn)
    for i in l:
      if not i['isdir']: tsize += i['size']

    return tsize


  def GetDir(self, remote, local):
    "get the remote directory, and save it under local path"

    old = self.smb.pwd()
    self.Chdir(remote)

    l = self.ListRecursive()
    
    for i in l:
      if not i['name'].startswith('\\'):
        i['name'] = "%s\\%s" % (remote, i['name'])
    
    sorted = self.SortFileList(l)
   
    # I have the sorted list here. Now, the procedure is
    # 1) create the local directory UNDER the local one
    # 2) chdir inside it
    # 3) create every directory in the path
    # 4) copy the files in the way.

    if remote != '' and remote != '\\':
      local = "%s/%s" % (local, os.path.basename(self.ToUNIX(remote)))
  
    for i in sorted:
    
     base = self.ToUNIX(i['val']['name'][len(remote)+1:]) # first '\\'
     lname = "%s/%s" % (local,base)
     lname = self.ToUNIX(lname)
     
     ldir = os.path.dirname(lname)

     if i['val']['isdir']:
       #
       # its a directory, so create it locally and go on
       #
       if not os.path.exists(lname):
         os.makedirs(lname, 0755)
     else:
       if not os.path.exists(ldir):
         os.makedirs(ldir, 0755)
       self.GetFile(i['val']['name'], lname)

    self.Chdir(old)

    return True

  def PutDir(self, local, remote):
    "puts the local directory inside the 'remote' one"

    flist = []
    for root, dirs, files in os.walk(local,topdown=True):

      for j in files:
        flist.append({ 'name': os.path.join(root,j) })


    sorted = self.SortFileList(flist,os.path.sep)

    # I have the sorted list here. Now, the procedure is
    # 1) create the remote directory
    # 2) chdir inside it
    # 3) create every directory in the path
    # 4) copy the files in the way.

    if local != '.':
      remote = "%s/%s" % (remote, os.path.basename(local))
      
    for i in sorted:
      lname = i['val']['name'][len(local):]

      rname = "%s/%s" % (remote, lname)
      rdir  = self.ToDOS(os.path.dirname(rname))
      rname = self.ToDOS(rname)
      
      self.Mkdir(rdir, True)
      #
      # copy inside
      #
      
      if not self.PutFile(i['val']['name'], rname):
        return False

    return True
    

  def GetFile_full(self,remote,local):
      "get the remote file remote and store it at local one"
        	
      try:
         fd = self.smb.open(remote,os.O_RDONLY)
	 data = self.smb.read(fd)
	 self.smb.close(fd)
	 ft = file(local,"wb+")
	 ft.write(data)
	 ft.close()
      except Exception, e:
       	 print "Error retrieving %s into %s: %s" % (remote,local,e)
	 return False
	
      return True


  def PutFile_full(self,local,remote):
      "put the local file local and store it at remote one"
        	
      try:
      
	 ft = file(local,"rb")
	 data = ft.read()
	 ft.close()
           
         fd = self.smb.open(remote,os.O_CREAT|os.O_TRUNC|os.O_RDWR)
	 self.smb.write(fd,0,os.path.getsize(local), data)
	 self.smb.close(fd)
	 
      except Exception, e:
       	 print "Error putting %s into %s: %s" % (local,remote,e)
	 return False
	
      return True



  def GetFile(self,remote,local, createdirs=False):
      "get the remote file remote and store it at local one do it by blocks"

      if createdirs:
        l = os.path.dirname(local)
        if not os.path.exists(l):
          os.makedirs( l, 0755 )

      try:
        fd = self.smb.open(remote,os.O_RDONLY)
        sz = self.smb.filesize(fd)

        ft = file(local,"wb+")

        chunks = sz / self.IOSZ
        offset = 0
      
        while True:
          goout = False
          chunk_sz = self.IOSZ

          if offset + chunk_sz > sz:
            chunk_sz = self.IOSZ - ((offset + chunk_sz) - sz)
            goout = True

          data = self.smb.read(fd,offset,chunk_sz)
          ft.write(data)

          offset += chunk_sz

          if goout:
            break

        self.smb.close(fd)
        ft.close()
         
      except Exception, e:
        print "Error retrieving %s into %s: %s" % (remote,local,e)
        return False
	
      return True


  def PutFile(self,local,remote, parent=False):
      "put the local file local and store it at remote one do it by blocks"

      if parent:
        #
        # create parent, if doesn't exists
        #
        b = self.ToDOS(os.path.dirname(self.ToUNIX(remote)))

        if not self.Exists(b):
          self.Mkdir(b,True)
        
        	
      try:
      
        ft = file(local,"rb")
      
        sz = os.path.getsize(local)

        fd = self.smb.open(remote,os.O_CREAT|os.O_TRUNC|os.O_RDWR)
      
        chunks = sz / self.IOSZ
        offset = 0
      
        while True:
          goout = False
          chunk_sz = self.IOSZ

          if offset + chunk_sz > sz:
            chunk_sz = self.IOSZ - ((offset + chunk_sz) - sz)
            goout = True
          
          data = ft.read(chunk_sz)
          self.smb.write(fd,offset,chunk_sz, data)
          offset += chunk_sz

          if goout:
            break

        ft.close()
        self.smb.close(fd)
	 
      except Exception, e:
        print "Error putting %s into %s: %s" % (local,remote,e)
        return False
      
      return True


  def Chdir(self, dir):
    "Changes to directory dir"

    if dir.find("\\") >= 0:
      items = dir.split("\\")

      for i in items:
        self.smb.chdir(i)

    try:
      self.smb.chdir(dir)
    except Exception, e:
      print "Error changing directory to %s: %s" % (dir, e)
      return False
    return True
        

  def Pwd(self):
    "Prints current working directory"
    return self.smb.pwd()


  def Unlink(self, fname):
    "Deletes file fname"
    return self.smb.unlink(fname)
    

  def Exists(self, fname):
    "Check if fname exists. Can be a directory or file"
    
    l = self.smb.exists(fname)
    return l == True

  def Mkdir(self, dirname, parent=False):
    "Creates a directory. if parent=True, intermediate dirs are created, too"
    
    if parent:
      #
      # for a given path, create every element in the
      # item, until a error is found. Note that the
      # strings come in DOS format.
      #
      items = dirname.split('\\')
      if not len(items):
        return False

      base = ""
      for i in items:
        base += i
        if not self.smb.exists(base):
          if not self.smb.mkdir(base):
            return False
        base += '\\'
      return True
        
    return self.smb.mkdir(dirname)


  def Rmdir(self, dirname, force=False):
    "Deletes a directory. If force is true, a rm -rf 'style' is done"
    
    if force:

      p = self.ToUNIX(dirname)
      dname = self.ToDOS(os.path.dirname(p))
      b = os.path.basename(p)

      self.Chdir(dname)
      dirname = b
      while True:

        if not self.smb.exists(dirname):
          return 

        item = self.ListRecursive(dirname)

        # foreach item in the list, remove them. file way
        for i in item:
          if not i['isdir']: self.smb.unlink(i['name'])

          # now, crunch every directory in the path. In
          # order to fix them I have to sort the entries
          # using the dir components
      
        item = self.ListRecursive(dirname)
        sorted = self.SortFileList(item)

        for i in range(0,len(sorted)):
          w = sorted[i]

          t = w['val']['name']
          if not t.startswith('\\'):
            # not full path
            t = self.ToDOS("%s/%s" % (dname, t))
          
          self.smb.rmdir(t)

    return self.smb.rmdir(dirname)

  # pretty print helpers ############################################
  
  def PrettyList(self,dir=None):
    "Shows a pretty directory list (like a dir)"
    
    print "\n%s" % self.Pwd()
    
    l = self.List(dir)
    for i in l:
      att = 'F'  
      if i['isdir']: att='D'
      print "%7d\t%c\t%s" % (i['size'], att, i['name'])
      
    print "Disk Available: %3.2f Mb\n" % (svr.DiskAvail()/(1024.0*1024.0))   

  def SortFileList(self, item, sep='\\'):
    "Sort a file list based on path length"
    
    sorted = []
    for i in item:
      sorted.append( { 'key': len(i['name'].split(sep))-1,
                       'val': i } )

    for i in range(0,len(sorted)-1):
      for j in range(i+1,len(sorted)):
        if sorted[i]['key'] < sorted[j]['key']:
          t = sorted[j]
          sorted[j] = sorted[i]
          sorted[i] = t

    return sorted

  def ToDOS(self,str):
    "Convert a path to a DOS style"
    
    w = re.sub("[/]+","\\\\",str)
    return w
  
  def ToUNIX(self,str):
    "Convert a path to a UNIX style"
    return w

  def GetCmdOutput(self,cmd):
    "Manages an external command using a pipe"
    p = os.popen(cmd, "r")
    data  = p.readlines()
    p.close()
    return data


