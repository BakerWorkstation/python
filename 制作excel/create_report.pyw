# -*- coding: cp936 -*-


import xlwt
import datetime
import urllib2
from xlwt import *

today = datetime.datetime.now().strftime("%Y%m%d")
font0 = Font()

font0.name = 'Times New Roman'

#font0.struck_out = True # 

font0.bold = True

badFontStyle = xlwt.XFStyle()
badFontStyle.font = font0


wb = Workbook(encoding='cp936')
ws0 = wb.add_sheet('报表数据',cell_overwrite_ok=True) # 可覆盖数据

all_list = [u'病毒分类',u'环境前缀',u'核心行为',u'家族名称',u'变种数量']
type_list = [u'木马',u'灰色软件',u'感染式病毒',u'风险软件',u'蠕虫',u'黑客工具',u'测试文件',u'垃圾文件']    


def compain():
    fnt=Font()
    fnt.colour_index= 4

    fnt.bold= True

    borders= Borders()

    borders.left= 0x1

    borders.right= 0x1

    borders.top= 0x1

    borders.bottom= 0x1

    style= XFStyle()

    style.font= fnt

    #style.borders = borders
    for k in range(0, 50):

        ws0.write_merge(0,1, k, k, '', style)

        ws0.col(1).width= 0x0d00

def format():
    #  ----单元格背景色-------  #
    badBG = xlwt.Pattern()
    badBG.pattern = badBG.SOLID_PATTERN
    badBG.pattern_fore_colour = 1
    #  ---------------------  #

    # ------字体颜色---------#
    font0.colour_index = 0x3f
   # font0.outline = True
    # ----------------------#

    # -------字体大小--------#
    font0.height = 250
    badFontStyle.font=font0
    badFontStyle.pattern = badBG
   
    # -----单元格边框------- #
    borders=Borders()
    borders.left=0x1
    borders.right=0x1
    borders.top=0x1
    borders.bottom=0x1
    #badFontStyle.borders=borders   
    # ---------------------- #


    for i in range(0, 100):

        for j in range(0,100):

            ws0.write(i, j,'',badFontStyle)
    ws0.write(0,1,'all',badFontStyle)
    ws0.row(0).set_style(badFontStyle)
    ws0.write(0,6,'type',badFontStyle)
    ws0.col(1).width = 0x0d00 + 2000
    ws0.col(6).width = 0x0d00 + 2000
    ws0.col(2).width = 0x0d00 + 1500
    ws0.col(7).width = 0x0d00 + 1500
    ws0.col(3).width = 0x0d00 + 3000
    ws0.col(8).width = 0x0d00 + 3000

        
def bluebg():
        #  ----单元格背景色-------  #
    font1 = Font()
    font1.bold = True
    font1.height = 200
    badFontStyle1 = xlwt.XFStyle()
    badFontStyle1.font = font1
    badBG = xlwt.Pattern()
    badBG.pattern = badBG.SOLID_PATTERN
    badBG.pattern_fore_colour = 49
    #  ---------------------  #
    font1.colour_index = 1
    badFontStyle1.pattern = badBG
   
    # -----单元格边框------- #
    borders=Borders()
    borders.left=0x1
    borders.right=0x1
    borders.top=0x1
    borders.bottom=0x1
    badFontStyle1.borders=borders   
    # ---------------------- #
    ws0.write(2,1,'类别',badFontStyle1)
    ws0.write(2,2,'总数',badFontStyle1)
    ws0.write(2,3,'本周新增数',badFontStyle1)
    ws0.write(2,6,'类别',badFontStyle1)
    ws0.write(2,7,'总样本/个',badFontStyle1)
    ws0.write(2,8,'本周新增数',badFontStyle1)
    print "done !"

def observe():
    font1 = Font()
    font1.bold = True
    font1.height = 200
    badFontStyle1 = xlwt.XFStyle()
    badFontStyle1.font = font1

    font1.colour_index = 0x3f
    borders=Borders()
    borders.left=0x1
    borders.right=0x1
    borders.top=0x1
    borders.bottom=0x1
    badFontStyle1.borders=borders
    for a in range(3, 8):
        for b in range(1, 4):
            ws0.write(a,b,'',badFontStyle1)
    for m in range(3,11):
        for n in range(6, 9):
            ws0.write(m,n,'',badFontStyle1)
    for x in range(0, 5):
        ws0.write(3+x,1,all_list[x],badFontStyle1)
    for v in range(0, 8):
        ws0.write(3+v,6,type_list[v],badFontStyle1)
    vt_f=open('F:/文档组周报/friday_report.txt','r')
    vtlines=[line.strip() for line in vt_f.readlines()]
    vt_f.close()

    zz=0
    for j in range(2,4):
        for l in range(3,8):
            ws0.write(l,j,vtlines[zz],badFontStyle1)
            zz=zz+1
    if j==3 and l==7:
        for o in range(7, 9):
            for p in range(3,11):
                ws0.write(p,o,vtlines[zz],badFontStyle1)
                zz=zz+1

def  catch_data():
    url = 'http://10.255.49.42/friday_report.txt'
    #print url
    h = urllib2.urlopen(url, timeout=20)
    buf = h.read()
    #print buf
    h.close()

    ff = open('F:/文档组周报/friday_report.txt', 'wb')
    ff.write(buf)
    ff.close
    
if __name__ == '__main__':
    catch_data()
    compain()
    ws0.insert_bitmap('F:/文档组周报/1.bmp', 2, 10)
    format()
    bluebg()
    observe()
    wb.save('F:/文档组周报/病毒样本库数据统计-'+today+'.xls')
    wb.save('C:/Users/admin/Desktop/病毒样本库数据统计-'+today+'.xls')
    


