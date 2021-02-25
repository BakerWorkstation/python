#!/usr/bin/env python
import leveldb

db = leveldb.LevelDB('./backup/master_table_default')
for i in db.RangeIter():
    if i[1] == '38':
        ff = open('./list_total.txt','ab')
        ff.write(i[0]+'\n')
ff.close()
