# -*- coding: utf-8 -*-

from tkSimpleDialog import * #进行输入验证
import Tkinter


import win32api
import pyHook
#from ctypes import *
import pythoncom 
import time
import os

#class POINT(Structure):
#    _fields_ = [("x", c_ulong),("y", c_ulong)]

#def get_mouse_point():
#    po = POINT()
#    windll.user32.GetCursorPos(byref(po))
#    return int(po.x), int(po.y)


#-------------------------------------------------over--------------------------------------------

def choice():
    top = Tkinter.Tk()
    top.title(unicode('鼠标坐标捕捉程序','utf-8'))
    top.configure(background = '#cdcdcd')
    #>>>>>>>>>>>>颜色面板
    #color = askcolor(title='颜色面板')
    #print(color)
    top.resizable(False, False)
    top.geometry("300x250+879+410")
    #top.attributes("-toolwindow", 1)

    position = Tkinter.Entry(
                            top, 
                            textvariable = 'username',
                            width="12",
                            #height = '2',
                            font=("宋体", 15, "normal")
                            )

    position.grid(row = 1,column = 1,padx = 0,pady = 15)

    def scan(choice):
        while 1:
            if choice == 'end':
                #top.destroy()
                #print 'quit'
                os._exit(0)

                #return
            if choice == 'start':
                def onMouseEvent(event):
                    # 监听鼠标事件   
                    #print "MessageName:",event.MessageName   
                    #print "Message:", event.Message   
                    #print "Time:", event.Time       
                    #print "Window:", event.Window   
                    #print "WindowName:", event.WindowName   
                    #print "Position:", event.Position   
                    position.delete(0,END)
                    position.insert(0,str(event.Position))
                    position.update()
                    #print "Wheel:", event.Wheel   
                    #print "Injected:", event.Injected      
                    #print"---"  
                    return True
 

            hm = pyHook.HookManager()
            #hm.HookKeyboard()               
            hm.MouseAll = onMouseEvent 
            hm.HookMouse()
            pythoncom.PumpMessages() 
            hm.UnhookMouse()     

    Tkinter.Button(
                    top,
                    text = '开始',
                    fg = 'blue',
                    bg = 'white',
                    width = '7',
                    height = '2',
                    font = ("宋体", 15,"normal"),
                    command = lambda : scan('start')).grid(row = 0, column = 0, padx = 4, pady = 20
                    )

    Tkinter.Button(
                    top,
                    text = '退出',
                    fg = 'blue',
                    bg = 'white',
                    width = '7',
                    height = '2',
                    font = ("宋体", 15,"normal"),
                    command = lambda : scan('end')).grid(row = 2, column = 2, padx = 4, pady = 20
                    )
    Tkinter.mainloop()


if  __name__  == '__main__':
    choice()
