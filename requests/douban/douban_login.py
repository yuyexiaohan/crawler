# coding=utf-8 
# Time : 2018/12/5
# Author : achjiang
from selenium import webdriver
import time
import requests
from requests.douban import dama
from requests.douban.settings import EMAIL, PASSWORD
from lxml import etree

"""
功能描述：实现自动登录豆瓣
"""

# 实例化driver
# driver = webdriver.Chrome(executable_path="‪E:\develop\chromedriver.exe")
driver = webdriver.Chrome(executable_path="chromedriver")
driver.get('https://www.douban.com/')

# 获取二级页面资源
html = driver.page_source
root = etree.HTML(html)
iframes = root.xpath('//div[contains(@class,"login")]/iframe/@src')[0]

# 重新获取登陆界面
driver.get('https:' + iframes)

driver.find_element_by_class_name("account-tab-account").click()
time.sleep(1)

driver.find_element_by_id("username").send_keys(EMAIL)
driver.find_element_by_id("password").send_keys(PASSWORD)

time.sleep(3)

# 判断识别验证码
try:
    captcha_image_url = driver.find_element_by_id("captcha_image").get_attribute("src")
except Exception as e:
    captcha_image_url = ''
# if captcha_image_url is not None:
#     captcha_content = requests.get(captcha_image_url).content
#
#     # 调用云打码平台
#     captcha_code = dama.indetify(captcha_content)
#     print('验证码的结果为:', captcha_code)
#
#     # 输入验证码
#     driver.find_element_by_id("captcha_field").send_keys(captcha_code)

# 点击登录按钮
driver.find_element_by_class_name("account-form-field-submit").click()

# 获取cookies
cookies = {i["name"]:i["value"] for i in driver.get_cookies()}
print(cookies)

time.sleep(15)

# 退出登录
driver.quit()

"""
uid: 68666
balance: 19990
cid: 1816454990, result: account
验证码的结果为: account
{'ap_v': '0,6.0', 'll': '"118254"', '__utmz': '30149280.1544011743.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)', 'bid': 'GMkzYg5ECc8', '_pk_ses.100001.8cb4': '*', '__utma': '30149280.1097530670.1544011743.1544011743.1544011743.1', 'dbcl2': '"77520740:+Fi/KaiT96k"', '__utmc': '30149280', '__utmt': '1', '_ga': 'GA1.2.1097530670.1544011743', '_gid': 'GA1.2.87628720.1544011764', '_gat_UA-7019765-1': '1', 'ck': 'cMtz', '_pk_id.100001.8cb4': '051bc31602acfe55.1544011741.1.1544011765.1544011741.', 'push_noty_num': '0', 'push_doumail_num': '0', '__utmv': '30149280.7752', '__utmb': '30149280.3.10.1544011743'}
"""