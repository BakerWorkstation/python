# -*- coding: cp936 -*-
import xlrd

#open the .xls file
xlsname="D:/病毒样本库数据统计-20150807.xlsx"
data = xlrd.open_workbook(xlsname,formatting_info=True)

table=data.sheets()[0]

cell=table.cell(2,1).value

#print value of the cell J141
print cell


from xlutils.copy import copy
 

#通过sheet_by_index()获取的sheet没有write()方法
rs = data.sheet_by_index(0)

wb = copy(data)

#通过get_sheet()获取的sheet有write()方法
ws = wb.get_sheet(0)
ws.write(2,2, 'changed!')
 
wb.save('D:\\1.xls')
