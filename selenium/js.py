# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import os
import time



chrome_driver_file = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chrome_driver_file

browser = webdriver.Chrome(executable_path=chrome_driver_file)
                             #chrome_options=chrome_options)
browser.maximize_window()
#browser.get('https://www.virustotal.com/intelligence/search/?query=engines%3A%22CVE-2010-2569%22')
browser.get('https://www.virustotal.com/')
time.sleep(3)



browser.find_element_by_xpath('//*[@id="mnu-signin"]/a').click()

browser.find_element_by_xpath('//*[@id="frm-signin"]/div/fieldset/div[1]/div[1]/input').send_keys(u'47385024@163.com')
browser.find_element_by_xpath('//*[@id="frm-signin"]/div/fieldset/div[2]/div[1]/input').send_keys(u'7788945a')

browser.find_element_by_xpath('//*[@id="btn-sign-in"]').click()


time.sleep(500)

f = open('./result.txt','ab')
f.write("CVE漏洞编号"+'\t\t'+"md5"+"\r\n")
f.close()

#browser.get('https://www.virustotal.com/intelligence/search/?query=engines%3A%22CVE-2010-2569%22')
for a in addr:
#while 1:
  url="https://www.virustotal.com/intelligence/search/?query=engines%3A%22" + a + "%22" 
  #print url

  browser.get(url)
  #browser.get('https://www.virustotal.com/intelligence/search/?query=engines%3A%22CVE-2004-0210%22')
  time.sleep(7)
  while 1:
    try:
      browser.find_element_by_id('btn-more-results').click()
      time.sleep(5)
    except:
      pass
      break
    #print a
  js = 'var q=document.body.scrollTop=0' 
  browser.execute_script(js) #页面回到最顶端
  time.sleep(1)

  browser.find_element_by_xpath('//*[@id="export-hashes"]').click()
  time.sleep(0.1)
  browser.find_element_by_xpath("//a[@href='#exported-hashes-md5']").click()
  data =  browser.find_element_by_id('exported-hashes-md5').text

  data = data.encode(encoding="utf-8")
  f = open('./result.txt','ab')
  print data
  if data == '':
    f.write(a + '\r\n')
  else:
    for i in data.split("\n"):
      f.write(a + '\t\t' + i + '\r\n')

  f.close()

