# coding=utf-8 
# Time : 2018/12/5
# Author : achjiang
from selenium import webdriver
import time
from yundama_python import *


EMAIL = "369668247@qq.com"
PASSWORD = "QAZwsx1992,.DB"

# 实例化driver
driver = webdriver.Chrome()
driver.get('https://www.douban.com/')

driver.find_element_by_id("form_email").send_keys(EMAIL)
driver.find_element_by_id("form_password").send_keys(PASSWORD)

time.sleep(5)

# 识别验证码

# 点击登录按钮
driver.find_element_by_class_name("bn-submit").click()

# 获取cookies
cookies = {i["name"]:i["value"] for i in driver.get_cookies()}
print(cookies)

time.sleep(5)

# 退出登录
driver.quit()
