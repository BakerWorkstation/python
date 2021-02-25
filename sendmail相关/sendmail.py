#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
homedir=os.getenv('test')

#要发给谁
mail_to="@qq.com"
mail_to1=".com"
mail_to2=".me"

def mime_text(smtp_from,smtp_to,subject,context):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject.decode('utf8')
    msg['From'] = smtp_from
    msg['To'] = smtp_to
    cc = context.decode('utf8')
    msg.attach(
        MIMEText(cc,"plain", "utf-8")
    )
    rt = msg.as_string()
    return rt


def send_mail(to_list,sub,content):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.163.com"
    mail_user=""
    mail_pass=""
    mail_postfix="163.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
#    msg = MIMEText(content)
    msg = MIMEMultipart("alternative")
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    cc = content.decode('utf8')
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, 
			mime_text(me, to_list, sub, content)
		)
        s.close()
        print '1'
        return True
    except Exception, e:
        print '2'
        print str(e)
        return False
if __name__ == '__main__':
    print sys.argv
    if send_mail(mail_to,"hello",sys.argv[1]):
        print "发送成功"
    else:
        print "发送失败"
    if send_mail(mail_to1,"hello",sys.argv[1]):
        print "发送成功"
    else:
        print "发送失败"
    if send_mail(mail_to2,"hello",sys.argv[1]):
        print "发送成功"
    else:
        print "发送失败"