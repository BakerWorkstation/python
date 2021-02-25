# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import time
import sys  

def auto_start(url,manul): 
    print 'ready'
    #chrome_to_mobile_plug_file =  "C:/Program Files (x86)/Google/Chrome/Application/Auto-Refresh_v0.2.crx"
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_extension(chrome_to_mobile_plug_file)

    chrome_driver_file = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chrome_driver_file

    browser = webdriver.Chrome(executable_path=chrome_driver_file)
                             #chrome_options=chrome_options)

    browser.maximize_window()
    time.sleep(1)
    browser.get(url)  
    time.sleep(0.1)

    if manul == 'whole_view':
        #time.sleep(0.1)
        #browser.find_element_by_id('uname').send_keys(u'test')
        #browser.find_element_by_id('passwd').send_keys(u'123')
        #browser.find_element_by_id('log').click()
        time.sleep(1)
        #browser.find_element_by_id('virusNet').click()
        while True:
            #browser.find_element_by_xpath("//*[text()='系统概况与图示']").click()
            #time.sleep(0.1)
            #browser.find_element_by_xpath("//a[@href='#main_data/']").click()
            #browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)
            browser.refresh()

    if manul == 'data_pandect':
        time.sleep(0.1)
        browser.find_element_by_id('uname').send_keys(u'test')
        browser.find_element_by_id('passwd').send_keys(u'123')
        browser.find_element_by_id('login_btn').click()
        time.sleep(1)
        browser.find_element_by_id('virusNet').click()
        time.sleep(1)
        while True:
            time.sleep(1)
            #browser.find_element_by_xpath("//*[text()='系统概况与图示']").click()
            #time.sleep(1)
            #browser.find_element_by_xpath("//a[@href='#homePage']").click()
            #browser.find_element_by_id('sidebar-collapse').click()
            browser.find_element_by_xpath("//*[text()='资源查询']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//*[text()='放马打击指数查询']").click()
            time.sleep(1)
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(3600)   
            browser.refresh()

    if manul == 'key_data':
        time.sleep(0.1)
        browser.find_element_by_id('uname').send_keys(u'test')
        browser.find_element_by_id('passwd').send_keys(u'123')
        browser.find_element_by_id('login_btn').click()
        time.sleep(0.1)
        browser.find_element_by_id('virusNet').click()
        time.sleep(1)
        while True:
            time.sleep(1)
            browser.find_element_by_xpath("//*[text()='系统概况与图示']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//a[@href='#main_data']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)
            browser.refresh()



    if manul == 'probe':
        time.sleep(0.1)
        browser.find_element_by_id('uname').send_keys(u'test')
        browser.find_element_by_id('passwd').send_keys(u'123')
        browser.find_element_by_id('login_btn').click()
        time.sleep(1)
        browser.find_element_by_id('virusNet').click()
        while True:
            time.sleep(1)
            browser.find_element_by_xpath("//*[text()='系统概况与图示']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//a[@href='#TF']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)
            browser.refresh()


  
if __name__ == '__main__':  
    auto_start(sys.argv[1],sys.argv[2])
    #auto_start('http://172.16.1.21/#/page/flow_diagram','run_condition')


    
