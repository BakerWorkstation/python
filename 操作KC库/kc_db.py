from kyotocabinet import *
import sys
import time

db = DB()
if not db.open("31.kch", DB.OREADER):
    print >>sys.stderr, "open error: " + str(db.error())

class VisitorImpl(Visitor):
    # call back function for an existing record
    def visit_full(self, key, value):
        if 'DDD4FA15795F17FCA00A53E0979E69A1.2041949B'  in key:
            ff = open(key, 'w')
            ff.write(value)
            ff.close()
        #print "%s:%s" % (key, value)
        #print "%s" % key
        #time.sleep(5)
        #print type(key)
        return self.NOP
    # call back function for an empty record space
    def visit_empty(self, key):
        #print >>sys.stderr, "%s is missing" % key
        return self.NOP
visitor = VisitorImpl()

for i in db.iterate(visitor, False):
        print >>sys.stderr, "iterate error: " + str(db.error())

if not db.close():
    print >>sys.stderr, "close error: " + str(db.error())
