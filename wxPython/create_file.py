# -*- coding: utf-8 -*-
import wx
import time



def scale():
    #app = wx.PySimpleApp()
    app = wx.App()
    progressMax = 100  
    dialog = wx.ProgressDialog("A progress box", "Time remaining", progressMax,  
            style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)  
    keepGoing = True  
    count = 0  
    while keepGoing and count < progressMax:  
        count = count + 1  
        #wx.Sleep(1)
        time.sleep(0.05)  
        if count == 100:
            dialog.Destroy()
            app.Destroy()
        keepGoing = dialog.Update(count)  
  
    #dialog.Destroy()

if __name__ == '__main__':

    #scale()

    def open_file(event):
        dlg = wx.MessageDialog(None, 'Are you sure to continue ?', 'Warning !' , wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == 5103:  # result : 5103 == True , 5104 == False
            file1 = open(filename.GetValue())
            contents.SetValue(file1.read())
            file1.close()
        

    def save_file(event):
        dlg = wx.MessageDialog(None, 'Is this the coolest thing ever!', 'Warning !' , wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == 5103:  # result : 5103 == True , 5104 == False
            file2 = open(filename.GetValue(), 'w')
            file2.write(contents.GetValue())
            file2.close()

    app = wx.App()
    win = wx.Frame(
                    #parent,
                    #id = -1,
                    None, 
                    title = 'test program', 
                    size = (410, 335)
                    )
    win.Centre()
    bkg = wx.Panel(win)
    Button1 = wx.Button(
                    bkg, 
                    label = 'open',
                    #pos = (225, 5),
                    #size = (80, 25)
                    )
    Button1.Bind(wx.EVT_BUTTON, open_file)

    Button2 = wx.Button(
                    bkg, 
                    label = 'save',
                    #pos = (315, 5),
                    #size = (80, 25)
                    )
    Button2.Bind(wx.EVT_BUTTON, save_file)

    filename = wx.TextCtrl(
                    bkg#, 
                    #pos = (5, 5),
                    #size = (210, 25)
                    )
    contents = wx.TextCtrl(
                    bkg,
                    #pos = (5, 35),
                    #size = (390, 260),
                    style = wx.TE_MULTILINE | wx.HSCROLL
                    )
    hbox = wx.BoxSizer()
    hbox.Add(filename, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
    hbox.Add(Button1, proportion = 0, flag = wx.LEFT, border = 5)
    hbox.Add(Button2, proportion = 0, flag = wx.LEFT, border = 5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox, proportion = 0, flag = wx.EXPAND | wx.ALL, border =5)
    vbox.Add(contents, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

    bkg.SetSizer(vbox)
    win.Show()

    app.MainLoop()
    