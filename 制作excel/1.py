# -*- coding: cp936 -*-
from xlrd import open_workbook
from xlutils.copy import copy



def catch_result_data():
    rb=open_workbook("D:/疑似误报MD5列表_result.xlsx")
    global md5_list_result
    md5_list_result = []
    for i in range(3):
        print i
        sheet=rb.sheet_by_index(i)
        j = 0
        while True:
            try:
                #print j
                md5_list_result.append(sheet.row_values(j, 0))
                j += 1
            except Exception as e:  
                print ' test : ' , str(e)
                break

def handle_data():
    rb1=open_workbook("D:/疑似误报MD5列表.xlsx")
    wb=copy(rb1)

    for x in range(6):
        sheet1=rb1.sheet_by_index(x)
        if x in (0,1,2):
            y = 1
        else:
            y = 0
        while True:
            #print sheet.row_values(1000, 0)
            try:
                for z in md5_list_result:
                    #print 'test'
                    #print type(sheet1.row_values(y,0)[0])
                    #print z[0]
                    if sheet1.row_values(y, 0)[0]  ==  z[0]:
                        #print 'ready'
                        ws=wb.get_sheet(x)
                        ws.write(y,2,z[2])
                        ws.write(y,3,z[3])
                        try:
                            ws.write(y,4,z[4])
                        except:
                            #ws.write(y,4,'')
                            #print 'no have E'
                            pass
                y += 1
            except Exception as e:
                print ' test : ' , str(e)
                break
    wb.save("D:/result.xls")
    
catch_result_data()
handle_data()

print len(md5_list_result)
