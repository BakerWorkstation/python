# -*- coding: cp936 -*-


import xlwt
import xlrd
import random
filename=xlwt.Workbook()
sheet=filename.add_sheet("my_sheet")
for row in range(0,10):
    for col in range(0,10):
        sheet.write(row,col,random.randrange(0,10))
filename.save("D:/test.xls")
print "Done"





import xlrd
filename="C:/Users/Administrator/Desktop/1U服务器测试.xlsx"
data=xlrd.open_workbook(filename)
sheet=data.sheet_by_index(0)
rows=sheet.nrows
cols=sheet.ncols
for row in range(rows):
    value=sheet.row_values(row)
    print value
import time
time.sleep(20)
