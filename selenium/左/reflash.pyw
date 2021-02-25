# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import win32api
from ctypes import *
import win32con

import os
import time
import sys  

def mouse_move(x,y):
    windll.user32.SetCursorPos(x, y)

def mouse_left_click(x=None, y=None, release=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.5)
    if release is None or release == 1:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def key_combination(hex_num):
    head = (hex_num/16)/16
    tail = hex_num % (16*16)
    if head == 0:
        win32api.keybd_event(tail,0,0,0)
        win32api.keybd_event(tail,0,win32con.KEYEVENTF_KEYUP,0)
    else:
        time.sleep(0.5)
        win32api.keybd_event(head,0,0,0)
        win32api.keybd_event(tail,0,0,0)
        win32api.keybd_event(head,0,win32con.KEYEVENTF_KEYUP,0)
        win32api.keybd_event(tail,0,win32con.KEYEVENTF_KEYUP,0)


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
    time.sleep(1)
    browser.find_element_by_id('uname').send_keys(u'test')
    browser.find_element_by_id('passwd').send_keys(u'123')
    browser.find_element_by_id('login_btn').click()
    time.sleep(1)

    if manul == 'run_condition':
        time.sleep(2)
        browser.find_element_by_id('sampleAnalysis_png').click()
        time.sleep(2)
        while True:            
            browser.find_element_by_xpath("//*[text()='子系统工作情况']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//a[@href='#/page/flow_diagram']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(80)   
            browser.refresh()

    if manul == 'key_data':
        time.sleep(2)
        browser.find_element_by_id('sampleAnalysis_png').click()
        time.sleep(2)
        while True:            
            browser.find_element_by_xpath("//*[text()='系统概况']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//a[@href='#/page/dashboard']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(80)
            browser.refresh()

    if manul == 'source_count':
        time.sleep(2)
        browser.find_element_by_id("sourceManage_png").click()
        time.sleep(2)
        while True:          
            time.sleep(1)
            browser.find_element_by_id('source_file_static').click()
            time.sleep(80)
            browser.refresh()

    if manul == 'source_total':
        time.sleep(2)
        browser.find_element_by_id('sampleAnalysis_png').click()
        time.sleep(2)
        mouse_left_click(965, 13,0)
        mouse_move(594, 559)
        mouse_left_click(594, 559)
        key_combination(0x7A)

        while True:            
            browser.find_element_by_xpath("//*[text()='系统概况']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//a[@href='#/page/report_sys']").click()
            browser.find_element_by_id('sidebar-collapse').click()
            time.sleep(80)
            browser.refresh()

  
if __name__ == '__main__': 
    auto_start(sys.argv[1],sys.argv[2])
    #auto_start('http://172.16.1.21/#/page/flow_diagram','run_condition')


    
