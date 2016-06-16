# coding=utf-8
import pdb

from selenium import webdriver
driver=webdriver.Chrome()
driver.get('http://www.baidu.com')
pdb.set_trace()
driver.close()