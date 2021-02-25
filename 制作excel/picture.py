# -*- coding: cp936 -*-
from xlwt import *

w = Workbook()

ws = w.add_sheet('Image')

ws.insert_bitmap('C:/Users/Administrator/Desktop/3.bmp', 2, 2)

w.save('image.xls')
