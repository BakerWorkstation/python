#!/usr/bin/env python
import leveldb

db = leveldb.LevelDB('/home/testdb')
#for i in db.RangeIter():
   # print i[:40]
string = db.Get('002427DDC22604C635322950165225FB.25B5D5BA')
ff = open('/root/12345','ab')
ff.write(string)
ff.close()
