# create a background image on a wxPython panel
# and show a button on top of the image
import os
import wx
import time
import wx.gizmos  as  gizmos
from subprocess import Popen
from wx.lib.ticker import Ticker
import wx.lib.colourselect as  csel  

#Popen("python reflash.pyw %s %s" % (url1,'data_pandect'),shell=True)


role = {}
#-------------------------------------------------------------------------------------------------
class Panel1(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent, id)
        try:
            # pick an image file you have in the working folder
            # you can load .jpg  .png  .bmp  or .gif files


            bg_file = './1.png'
            bg = wx.Image(bg_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            
            login_file =  './login.jpg'
            #login_file = './2.png'
            self.login = wx.Image(login_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            create_file = './create.jpg'
            self.create = wx.Image(create_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            delete_file = './delete.jpg'
            self.delete = wx.Image(delete_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            ch_pwd_file = './change_pwd.jpg'
            self.ch_pwd = wx.Image(ch_pwd_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            quit_file = './quit.jpg'
            self.quit = wx.Image(quit_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            # image's upper left corner anchors at panel coordinates (0, 0)
            self.bitmap1 = wx.StaticBitmap(self, -1, bg, (0, 0))
            # show some image details


            led = gizmos.LEDNumberCtrl(self, -1, (1, 1), (210, 50),
                              gizmos.LED_ALIGN_CENTER) #| gizmos.LED_DRAW_FADED)
            led.SetBackgroundColour("black")

            led.SetForegroundColour("magenta")
            self.clock = led
            self.OnTimer(None)

            self.timer = wx.Timer(self)
            self.timer.Start(1000)
            self.Bind(wx.EVT_TIMER, self.OnTimer)

            str1 = "%s  %dx%d" % (bg_file, bg.GetWidth(), bg.GetHeight())


            #self.info = wx.InfoBar(self)
            #self.message = wx.TextCtrl(self, -1, ' '*90 + "Hello World" , size=(800,-1))
            #msg = self.message.GetValue()
            #flag = flags[self.flags.GetSelection()][0]
            #self.info.ShowMessage(msg)#, flag)
            #self.info.Dismiss()


            #--------------------------------------------------------------------------------
            '''
            self.ticker = Ticker(self)

            #       Do layout
            sz = wx.FlexGridSizer(cols=20, hgap=40, vgap=40)
        

        
            sz2 = wx.BoxSizer(wx.VERTICAL)
            sz2.Add(self.ticker, flag=wx.EXPAND|wx.ALL, border=5)
            sz2.Add(sz, flag=wx.EXPAND|wx.ALL, proportion=1, border=25)
            self.SetSizer(sz2)
            sz2.SetSizeHints(self)
            self.ticker.SetText('Welcome    to    Dota2')
            

            '''
            #--------------------------------------------------------------------------------
            #parent.SetTitle(str1)
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit
            
    def OnTimer(self, evt):
        t = time.localtime(time.time())
        st = time.strftime("%I-%M-%S", t)
        self.clock.SetValue(st)

        # button goes on the image --> self.bitmap1 is the parent
        #self.button1 = wx.Button(self.bitmap1, id=-1, label='Button1', pos=(8, 8))

    def onshow(self):
        name = wx.StaticText(
                    self.bitmap1, 
                    label = "Username",
                    pos = (280, 200),
                    #size = (58, 18),
                    )
        font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD)
        name.SetFont(font)
        name.SetForegroundColour('green')  
        name.SetBackgroundColour('black')  


        pd = wx.StaticText(
                    self.bitmap1, 
                    label = "password",
                    pos = (280, 250),
                    #size = (58, 17),
                    )

        pd.SetFont(font)
        pd.SetForegroundColour('green')  
        pd.SetBackgroundColour('black')

        bg1 = self.username_input = wx.TextCtrl(
                    self.bitmap1, 
                    pos = (370, 198),
                    size = (150, 25)
                    )
        bg1.SetFont(font)
        bg1.SetBackgroundColour('black')
        bg1.SetForegroundColour('red')

        pd.SetForegroundColour('green') 
        bg2 = self.password_input = wx.TextCtrl(
                    self.bitmap1, 
                    pos = (370, 248),
                    size = (150, 25)
                    )
        bg2.SetFont(font)
        bg2.SetBackgroundColour('black')
        bg2.SetForegroundColour('red')

        login = wx.BitmapButton(self.bitmap1, -1, self.login, pos=(310,330))
        login.Bind(wx.EVT_BUTTON, login1)

        create = wx.BitmapButton(self.bitmap1, -1, self.create, pos=(640,400))
        create.Bind(wx.EVT_BUTTON, create1)

        delete = wx.BitmapButton(self.bitmap1, -1, self.delete, pos=(640,450))
        delete.Bind(wx.EVT_BUTTON, delete1)

        change = wx.BitmapButton(self.bitmap1, -1, self.ch_pwd, pos=(640,500))
        change.Bind(wx.EVT_BUTTON, change1)

        quit1 = wx.BitmapButton(self.bitmap1, -1, self.quit, pos=(15,500))
        quit1.Bind(wx.EVT_BUTTON, quit_)

#-----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #app = wx.PySimpleApp()
    app = wx.App()
    # create a window/frame, no parent, -1 is default ID
    # change the size of the frame to fit the backgound images
    frame1 = wx.Frame(None, -1, title = "Dota2 client (english) ", size=(800, 600))

    icon = wx.Icon('exe.ico', wx.BITMAP_TYPE_ICO)

    frame1.SetIcon(icon)


#----------------- scale ------------------------------------------------------------------------------
    def scale1(event):
        progressMax = 100
        dialog = wx.ProgressDialog(
                                "A progress box",
                                "Time remaining",
                                progressMax, 
                                style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME
                                )
        keepGoing = True
        count = 0
        while keepGoing and count < progressMax:
            count = count + 1
            time.sleep(0.01)
            if count == 100:
                dialog.Destroy()
                break
            keepGoing = dialog.Update(count)



    def login1(event):
        nm = panel1.username_input.GetValue()
        pd = panel1.password_input.GetValue()
        if nm == '':
            if pd == '':
                wx.MessageBox("Please input username and password " , "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

            else:
                wx.MessageBox("Please input username" , "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

        else:
            if pd == '':
                wx.MessageBox("Please input password" , "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

            if not role.has_key(nm):
                wx.MessageBox("username is not exist" , "Message" ,wx.OK | wx.ICON_INFORMATION)
            try:
                if role[nm] != pd:
                    wx.MessageBox("password not right, try again" , "Message" ,wx.OK | wx.ICON_INFORMATION)
                    return 0
            except Exception as e:
                return 0
        scale1(event)
        print nm,pd
        wx.MessageBox("'%s' login successfully" % nm, "Message" ,wx.OK | wx.ICON_INFORMATION)
        frame1.Destroy()
        #time.sleep(3)
        cmd = 'cmd.exe /k python ./snake.py'
        #os.system(cmd)
        Popen("python ./snake.py",shell=True)  # master program still alive
    
    def create1(event):
        a = wx.Dialog(None, title = 'create ?', size = (250,150))
        panel = wx.Panel(a)
        btn3 = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,30), pos = (50,80))
        btn4 = wx.Button(panel, wx.ID_CANCEL, label = "cancel", size = (50,30), pos = (130,80))


        username1 = wx.StaticText(
                    panel,
                    label = "Username ",
                    pos = (5, 5),
                    size = (70, 25),
                    )

        user_input1 = wx.TextCtrl(
                    panel,
                    pos = (85, 5),
                    size = (150, 25)
                    )

        password1 = wx.StaticText(
                    panel, 
                    label = "Password ",
                    pos = (5, 40),
                    size = (70, 25),
                    )

        passwd_input1 = wx.TextCtrl(
                    panel, 
                    pos = (85, 40),
                    size = (150, 25)
                    )

        b = a.ShowModal()

        if b == 5101:
            return 0
        if user_input1.GetValue() == '':
            wx.MessageBox("username can`t be NULL", "Message" ,wx.OK | wx.ICON_INFORMATION)
            return 0
        else: 
            if passwd_input1.GetValue() == '':
                wx.MessageBox("password can`t be NULL", "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0
            if user_input1.GetValue() not in role:
                scale1(event)
                role[user_input1.GetValue()] = passwd_input1.GetValue()
                wx.MessageBox("'%s' create successfully" % user_input1.GetValue(), "Message" ,wx.OK | wx.ICON_INFORMATION)
                #print role
            else:
                wx.MessageBox("'%s' has been exist" % user_input1.GetValue(), "Message" ,wx.OK | wx.ICON_INFORMATION)

    def delete1(event):  
        a = wx.Dialog(None, title = 'delete ?', size = (250,150))
        panel = wx.Panel(a)
        btn3 = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,30), pos = (50,80))
        btn4 = wx.Button(panel, wx.ID_CANCEL, label = "cancel", size = (50,30), pos = (130,80))

        username1 = wx.StaticText(
                    panel, 
                    label = "Username ",
                    pos = (5, 5),
                    size = (70, 25),
                    )

        user_input1 = wx.TextCtrl(
                    panel, 
                    pos = (85, 5),
                    size = (150, 25)
                    ) 

        password1 = wx.StaticText(
                    panel,
                    label = "Password ",
                    pos = (5, 40),
                    size = (70, 25),
                    )

        passwd_input1 = wx.TextCtrl(
                    panel,
                    pos = (85, 40),
                    size = (150, 25)
                    )

        b = a.ShowModal()

        if b == 5101:
            return 0
        #print user_input1.GetValue()
        #print passwd_input1.GetValue()
        if user_input1.GetValue() == '':
            wx.MessageBox("username can`t be NULL", "Message" ,wx.OK | wx.ICON_INFORMATION)
            return 0
        else:
           
            if role.has_key(user_input1.GetValue()):
                if role[user_input1.GetValue()] == passwd_input1.GetValue():
                    scale1(event)
                    role.pop(user_input1.GetValue())
                    wx.MessageBox("'%s' delete successfully" % user_input1.GetValue(), "Message" ,wx.OK | wx.ICON_INFORMATION)

                else:
                    wx.MessageBox("password isn`t right", "Message" ,wx.OK | wx.ICON_INFORMATION)
                    return 0
            else:
                wx.MessageBox("'%s' has not been exist" % user_input1.GetValue(), "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

    def change1(event):
        a = wx.Dialog(None, title = 'change ?', size = (250,150))
        panel = wx.Panel(a)
        btn3 = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,30), pos = (50,80))
        btn4 = wx.Button(panel, wx.ID_CANCEL, label = "cancel", size = (50,30), pos = (130,80))


        username1 = wx.StaticText(
                    panel,
                    label = "Username ",
                    pos = (5, 5),
                    size = (70, 25),
                    )

        user_input1 = wx.TextCtrl(
                    panel,
                    pos = (85, 5),
                    size = (150, 25)
                    )

        password1 = wx.StaticText(
                    panel,
                    label = "Password ",
                    pos = (5, 40),
                    size = (70, 25),
                    )

        passwd_input1 = wx.TextCtrl(
                    panel,
                    pos = (85, 40),
                    size = (150, 25)
                    )

        b = a.ShowModal()

        if b == 5101:
            return 0
        #print user_input1.GetValue()
        #print passwd_input1.GetValue()
        if user_input1.GetValue() == '':
            wx.MessageBox(
                            "username can`t be NULL", 
                            "Message",
                            wx.OK | wx.ICON_INFORMATION
                            )
            return 0
        else:
            if role.has_key(user_input1.GetValue()):
                if role[user_input1.GetValue()] == passwd_input1.GetValue():
                    c = wx.Dialog(None, title = 'delete ?', size = (250,150))
                    panel = wx.Panel(c)
                    btn3 = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,30), pos = (50,80))
                    btn4 = wx.Button(panel, wx.ID_CANCEL, label = "cancel", size = (50,30), pos = (130,80))


                    password2 = wx.StaticText(
                                            panel,
                                            label = "new password",
                                            pos = (5, 5),
                                            size = (100, 25),
                                            )
                    pwd_input2 = wx.TextCtrl(
                                            panel,
                                            pos = (105, 5),
                                            size = (130, 25)
                                            )
                    d = c.ShowModal()
                    if d == 5101:
                        return 0
                    if d == 5100:
                        if pwd_input2.GetValue() == '':
                            wx.MessageBox("password can`t be null", "Message" ,wx.OK | wx.ICON_INFORMATION)
                            return 0
                        role[user_input1.GetValue()] = pwd_input2.GetValue()
                        scale1(event)
                        wx.MessageBox("password change successfully", "Message" ,wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("password isn`t right", "Message" ,wx.OK | wx.ICON_INFORMATION)
                    return 0
            else:
                wx.MessageBox("'%s' has not been exist" % user_input1.GetValue(), "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

            if passwd_input1.GetValue() == '':
                wx.MessageBox("password can`t be NULL", "Message" ,wx.OK | wx.ICON_INFORMATION)
                return 0

    def quit_(event):
        frame1.Destroy()
    
#-------------------------------------------------------------------------------------------------------
    #def create1(event):
    # create the class instance
    panel1 = Panel1(frame1, -1)
    panel1.onshow()

    frame1.Centre()
    frame1.SetMaxSize((800, 600))
    frame1.SetMinSize((800, 600))
    frame1.Show(True)
    
    app.MainLoop()