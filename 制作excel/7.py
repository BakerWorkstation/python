from xlwt import *
import xlwt
font0 = Font()

font0.name = 'Times New Roman'

#font0.struck_out = True

font0.bold = True

style0 = XFStyle()

style0.font = font0

wb = Workbook()

ws0 = wb.add_sheet('0')

badBG = xlwt.Pattern()
badBG.pattern = badBG.SOLID_PATTERN
badBG.pattern_fore_colour = 49

badFontStyle = xlwt.XFStyle()
badFontStyle.font = font0
badFontStyle.pattern = badBG

borders=Borders()
borders.left=0x1
borders.right=0x1
borders.top=0x1
borders.bottom=0x1
badFontStyle.borders=borders

ws0.write(1, 1, 'Test', style0)

for i in range(0, 0x53):

    fnt = Font()

    fnt.name = 'Arial'

    fnt.colour_index = i

    fnt.outline = True

    borders = Borders()

    borders.left = i

    style = XFStyle()

    style.font = fnt

    style.borders =borders

    ws0.write(i, 2,'colour', style)

    ws0.write(i, 3,hex(i),badFontStyle)

wb.save('format.xls')
