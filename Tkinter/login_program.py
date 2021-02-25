# -*- coding: utf-8 -*-

#f=open('C:\\Users\\Administrator\\Desktop\\apsc_client_ui.ini','r')
#g=open('C:\\Users\\Administrator\\Desktop\\123.txt','w')
#for i in range(6):
#        data = f.readline().strip().decode(encoding="utf-8")
#        data = data.encode(encoding="utf-8")
#        print data
#        g.write(data+'\n')
#g.close()        
#f.close()


#from Tkinter import *
#from tkColorChooser import askcolor 

from SimpleDialog import *
from tkMessageBox import *
from tkSimpleDialog import * #进行输入验证
import Tkinter
import tkMessageBox   #验证成功弹窗       
#from PIL import Image, ImageTk
import psycopg2
import threading
import time



def  connect_pgdata(name_data=None,passwd_data=None,manua=None):
        cxn = psycopg2.connect(
                    host = '10.255.40.245',
                    user = 'postgres',
                    password = 'postgres',
                    database = 'test'
                    )
        cur = cxn.cursor()

        if manua == 'select':
                data='\'' + name_data + '\''
                sql = "select * from  account where name = %s" % data
                cur.execute(sql,data)
                rows = cur.fetchall()
                print rows
                return rows
                
        if manua == 'insert':
                data = (name_data,passwd_data)
                sql = "insert into account values ('%s','%s')"  %  data
                cur.execute(sql,data)

        if manua == 'change':
                data = (passwd_data,name_data)
                sql = "update account set passwd = '%s' where name = '%s'"  %  data
                cur.execute(sql,data)

        if manua == 'delete':
                data = name_data
                sql = "delete from account where name = \'%s\'"  %  data
                cur.execute(sql,data)

        cur.close()
        cxn.commit()
        cxn.close()
        #if manue == 'select': return rows

#-------------------------------------------------over--------------------------------------------

class Dialog(Toplevel):

    def __init__(self, parent, title = '请输入验证'):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)
    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        Label(master, text="用户名:").grid(row=0)
        Label(master, text="密  码:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        wa = Button(
                        box,
                        text="OK", 
                        width=10, 
                        command=self.ok, 
                        default=ACTIVE
                        )
        wa.pack(side=LEFT, padx=5, pady=5)

        wb = Button(
                        box, 
                        text="Cancel", 
                        width=10, 
                        command=self.cancel
                        )
        wb.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.parent.focus_set()
        self.destroy()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        return 
    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        first = str(self.e1.get())
        second = str(self.e2.get())
        self.tab = [first,second]

        del_e1 = self.e1.delete(0,END)
        del_e2 = self.e2.delete(0,END)
        self.delete = [del_e1,del_e2]

        return # override

# ------------------------------------------over--------------------------------------------
def process_auto(delay):    
                process = Toplevel()
                process.title(unicode('处理中,请稍候......','utf-8'))
                process.geometry("400x80+450+400")
                #process.iconbitmap('C:/Users/Burning/Desktop/1.ico')
                
                pro = Scale(
                        process,
                        from_ = 0,
                        to = 100.0,
                        orient = HORIZONTAL,
                        label = '当前进度',
                        fg = 'red',
                        width = '20',
                        length = '370'
                        )

                pro.set('0')
                pro.grid(row = 3, column = 0, padx = 15, pady = 10)
                for i in range(1,101):
                        pro.set(i)
                        pro.update()
                        time.sleep(float(delay))
                process.destroy()

#------------------------------------------over---------------------------------------
def send(default,choice):
        list_napw = Dialog(default)
        try:
                name,passwd = list_napw.tab
        except AttributeError ,e:
                #print 'test:' + str(e)
                return
        print name
        print passwd


        if choice == 'create':

                if '' == name:
                        tkMessageBox.showinfo("创建用户","创建失败，用户名不能为空！")
                        return
                if '' == passwd:
                        tkMessageBox.showinfo("创建用户","创建失败，密码不能为空！")
                        return
                
                if  len(connect_pgdata(name,manua='select')) == 0:
                        connect_pgdata(name,passwd,'insert')              
                        T1 = threading.Thread(target=process_auto(0.009))
                        T1.start()
                        tkMessageBox.showinfo("创建用户","用户 "+ name + " 创建成功！")
                        return
                else:
                        tkMessageBox.showinfo("创建用户","创建失败，用户已存在！")
                        return

        elif choice == 'login':
                try:
                        if name == connect_pgdata(name,manua='select')[0][0].strip():

                                if passwd == connect_pgdata(name,manua='select')[0][1].strip():
                                        T2 = threading.Thread(target=process_auto(0.009))
                                        T2.start()
                                        tkMessageBox.showinfo("登录用户","用户 "+ name +" 登录成功！")
                                else:
                                        tkMessageBox.showinfo("登录用户","登录失败,密码错误!")

                        else:
                                tkMessageBox.showinfo("登录用户","登录失败,用户不存在!")
                except IndexError ,e:
                        #print 'test' + str(e)
                        tkMessageBox.showinfo("登录用户","登录失败,用户不存在!")
                        pass
        elif choice == 'change':
                try:
                        if name == connect_pgdata(name,manua='select')[0][0].strip():
                                if passwd == connect_pgdata(name,manua='select')[0][1].strip():
                                        new_passwd = askstring(title = '验证成功',prompt = '请输入新密码:')
                                        connect_pgdata(name,new_passwd,manua='change')
                                        T3 = threading.Thread(target=process_auto(0.005))
                                        T3.start()
                                        tkMessageBox.showinfo("更改密码","更改成功")
                                else:
                                        tkMessageBox.showinfo("更改密码","验证失败")

                except IndexError ,e:
                        #print 'test:' + str(e)
                        tkMessageBox.showinfo("更改密码","更改失败,用户不存在!")
                        pass
        elif choice == 'delete':
                try:
                        if name == connect_pgdata(name,manua='select')[0][0].strip():
                                if passwd == connect_pgdata(name,manua='select')[0][1].strip():
                                        connect_pgdata(name,manua='delete')
                                        T4 = threading.Thread(target=process_auto(0.009))
                                        T4.start()
                                        tkMessageBox.showinfo("删除用户","用户 "+ name + " 删除成功!")
                                else:
                                        tkMessageBox.showinfo("删除用户","删除失败，密码错误!")
                        else:
                                tkMessageBox.showinfo("删除用户","删除失败，用户不存在!")
                except IndexError ,e:
                        #print 'test:' + str(e)
                        tkMessageBox.showinfo("删除用户","删除失败，用户不存在!")
                        pass
        list_napw.delete #数值使用后 初始化

#-------------------------------------------------over--------------------------------------------

def choice():
        top = Tkinter.Tk()
        top.title(unicode('游戏登录程序','utf-8'))
        top.configure(background = '#6f50a0')
        #>>>>>>>>>>>>颜色面板
        #color = askcolor(title='颜色面板')
        #print(color)
        top.resizable(False, False)
        top.geometry("700x500+700+400")
        #top.attributes("-toolwindow", 1)
        #top.iconbitmap('C:/Users/Burning/Desktop/1.ico')
        img = PhotoImage(file = "c:/Users/admin/Desktop/1.gif") 
        Label(top, text = "abc", image = img).grid(row = 1, column = 0, padx = 0, pady = 0)


        def quit():
                value = askokcancel(
                        title = '退出程序',
                        message = '你确定要退出吗？',
                        default = CANCEL # 指定默认焦点位置  #ABORT/RETRY/IGNORE/OK/CANCEL/YES/NO
                )
                if value == True: top.destroy()


        Tkinter.Button(
                        top,text = '创建账户',
                        fg = 'red',
                        bg = 'white',
                        width = '15',
                        height = '2',
                        font = ("宋体", 17,"normal"),
                        command = lambda :  send(top,'create')).grid(row = 0, column = 1, padx = 80, pady = 5
                        )#.pack(side=Tkinter.TOP)
        Tkinter.Button(
                        top,
                        text = '登录账户',
                        fg = 'blue',
                        bg = 'white',
                        width = '15',
                        height = '2',
                        font = ("宋体", 17,"normal"),
                        command = lambda : send(top,'login')).grid(row = 1, column = 1, padx = 15, pady = 0
                        )#.pack(side=Tkinter.LEFT)
        Tkinter.Button(
                        top,
                        text = '更改密码',
                        fg = 'green',
                        bg = 'white',
                        width = '15',
                        height = '2',
                        font = ("宋体", 17,"normal"),
                        command = lambda : send(top,'change')).grid(row = 3, column = 0, padx = 0, pady = 5
                        )#.pack(side=Tkinter.LEFT)
        Tkinter.Button(
                        top,
                        text = '删除账户',
                        fg = 'black',
                        bg = 'white',
                        width = '15',
                        height = '2',
                        font = ("宋体", 17,"normal"),
                        command = lambda : send(top,'delete')).grid(row = 2, column = 1, padx = 15, pady = 0
                        )#.pack(side=Tkinter.RIGHT)
        Tkinter.Button(
                        top,
                        text = '退出',
                        fg = 'brown',
                        bg = 'white',
                        width = '15',
                        height = '2',
                        font = ("宋体", 17,"normal"),
                        command = lambda : quit()).grid(row = 4, column = 1, padx = 15, pady = 4
                        )#.pack(side=Tkinter.BOTTOM)

        Tkinter.mainloop()

if  __name__  == '__main__':
        choice()



#----------------------------------------------OVER-----------------------------------------------
'''
def old_item(choose):
        def send(default):
                #a,b = username.get('0.0', END),password.get('0.0', END)
                #a,b = username.get(),password.get()
                username = askstring(title = 'string',prompt = 'input a string')
                password = askstring(title = 'string',prompt = 'input a string')
                print username
                print password
                if default == 'create':
                        if '\n' == b:
                                username.delete(0,END)
                                password.delete(0,END)
                                child.destroy()
                                tkMessageBox.showinfo("创建用户","创建失败，密码不能为空！")
                                return
                        if  a  not in role:
                                print a,b
                                role[a] = b
                                #username.delete('0.0',END)
                                username.delete(0,END)
                                #password.delete('0.0',END)
                                password.delete(0,END)
                                child.destroy()
                                process_auto()
                                tkMessageBox.showinfo("创建用户","用户 "+ a + " 创建成功！")
                        else:
                                username.delete(0,END)
                                password.delete(0,END)
                                child.destroy()
                                tkMessageBox.showinfo("创建用户","创建失败，用户名已存在！")
                elif default == 'login':
                        if a in role:
                                if b == role[a]:
                                        username.delete(0,END)
                                        password.delete(0,END)
                                        child.destroy()
                                        process_auto()
                                        tkMessageBox.showinfo("登录用户","用户 "+ a +" 登录成功！")
                                else:
                                        username.delete(0,END)
                                        password.delete(0,END)
                                        child.destroy()
                                        tkMessageBox.showinfo("登录用户","登录失败,密码错误!")
                        else:
                                username.delete(0,END)
                                password.delete(0,END)
                                child.destroy()
                                tkMessageBox.showinfo("登录用户","登录失败,用户名不存在!")
                elif default == 'delete':
                        if a in role:
                                if b == role[a]:
                                        role.pop(a)
                                        username.delete(0,END)
                                        password.delete(0,END)
                                        child.destroy()
                                        process_auto()
                                        tkMessageBox.showinfo("删除用户","用户 "+ a + " 删除成功!")
                                else:
                                        username.delete(0,END)
                                        password.delete(0,END)
                                        child.destroy()
                                        tkMessageBox.showinfo("删除用户","删除失败，密码错误!")
                        else:
                                username.delete(0,END)
                                password.delete(0,END)
                                child.destroy()
                                tkMessageBox.showinfo("删除用户","删除失败，用户不存在!")
                      
        #child = Tk()
        #child=Toplevel()
        #title = child.title(unicode('请输入验证！','utf-8'))
        #child.iconbitmap('C:/Users/Burning/Desktop/1.ico')
        #child.geometry("300x80+600+500")
        
        #dlg = SimpleDialog(child,
        #        text = 'hello SimpleDialog',
        #        buttons = ['Yes','No','cancel'],
        #        default = 0,
        #        )
        #print dlg.go()
        
        #print askinteger(title = 'prompt',prompt = 'input a integer:',initialvalue = 100)
        #print askfloat(title = 'float',prompt = 'input a float',minvalue = 0,maxvalue = 11)

        #Label(child,text = '用户名').grid(row = 4,column = 1,padx = 5)
        #Label(child,text = '密  码').grid(row = 5,column = 1,padx = 5)
        
        #username =  Text(child,width = '20',height = '1')
        #username =  Tkinter.Entry(child, textvariable = 'username',width="20",font=("宋体", 12, "normal"))
        #username.grid(row = 4,column = 2,padx = 5)
 
        #password =  Text(child,width = '20',height = '1')
        #password =  Tkinter.Entry(child, textvariable = 'password',width="20",font=("宋体", 12, "normal"))
        #password.grid(row = 5,column = 2,padx = 5)
        #button = Button(child,text = '发 送',width='6',height='1')#,command= lambda : send(choose))
        #button.grid(row = 6,column = 1,padx = 5,pady = 5)
        #button.bind('<Enter>',send(choose))
'''