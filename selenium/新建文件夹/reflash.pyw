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
    time.sleep(2)
    browser.find_element_by_id('uname').send_keys(u'test')
    browser.find_element_by_id('passwd').send_keys(u'123')
    browser.find_element_by_id('login_btn').click()

    if manul == 'run_condition':
        time.sleep(30)
        while True:
            browser.refresh()
            browser.find_element_by_xpath("//*[text()='子系统工作情况']").click()
            time.sleep(0.1)
            browser.find_element_by_xpath("//a[@href='#/page/flow_diagram']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)   

    if manul == 'key_data':
        time.sleep(30)
        while True:
            browser.refresh()
            browser.find_element_by_xpath("//*[text()='系统概况']").click()
            time.sleep(0.1)
            browser.find_element_by_xpath("//a[@href='#/page/dashboard']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)

    if manul == 'source_count':
        time.sleep(30)
        while True:
            browser.refresh()
            time.sleep(0.1)
            browser.find_element_by_id('source_file_static').click()
            time.sleep(30)

    if manul == 'source_total':
        time.sleep(30)
        while True:
            browser.refresh()
            browser.find_element_by_xpath("//*[text()='系统概况']").click()
            time.sleep(0.1)
            browser.find_element_by_xpath("//a[@href='#/page/report_sys']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(30)


  
if __name__ == '__main__':  
    auto_start(sys.argv[1],sys.argv[2])
    #auto_start('http://172.16.1.21/#/page/flow_diagram','run_condition')


    
