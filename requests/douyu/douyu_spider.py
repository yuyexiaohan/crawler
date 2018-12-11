# coding=utf-8 
# Time : 2018/12/6
# Author : achjiang

from selenium import webdriver
import time
import json

class DouyuSpider():
	"""斗鱼"""
	def __init__(self):
		self.start_url = "https://www.douyu.com/directory/all"
		# self.driver = webdriver.Chrome(executable_path="‪E:\develop\chromedriver.exe")
		self.driver = webdriver.Chrome()

	def get_content_list(self):
		"""获取数据"""
		li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
		content_list = []
		for li in li_list:
			item = {}
			item["room_img"] = li.find_element_by_xpath(".//span[@class='imgbox']/img").get_attribute("src")
			item["room_title"] = li.find_element_by_xpath("./a").get_attribute("title")
			item["room_cate"] = li.find_element_by_xpath(".//span[@class='tag ellipsis']").text
			item["anchor_name"] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
			item["watch_num"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
			print('item:', item)
			"""
				item: {'room_img': 'https://rpic.douyucdn.cn/asrpic/181206/99999_0134.jpg/dy1', 
				'room_title': '今晚人家真的很有感觉', 'room_cate': 'DNF', 
				'anchor_name': '旭旭宝宝', 'watch_num': '392万'}
			"""
			content_list.append(item)
		# 获取下一页元素,注意这里使用.find_elements_by_xpath,有s返回时一个数组
		next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
		next_url = next_url[0] if len(next_url)>0 else None
		return content_list, next_url

	def save_content_list(self, content_list):
		"""报错数据"""
		file_path = "斗鱼" + ".txt"
		with open(file_path, "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")
		print("保存成功")

	def run(self):
		"""循环"""
		# 1.start_url
		# 2.发送请求，获取响应
		self.driver.get(self.start_url)
		# 3.提取数据及下一页元素
		content_list, next_url = self.get_content_list()
		# 4.保存数据
		self.save_content_list(content_list)
		# 5.点击下一页元素，循环
		while next_url is not None:
			next_url.click()
			# 强制停止,方便数据加载
			time.sleep(3)
			content_list, next_url = self.get_content_list ()
			self.save_content_list(content_list)

if __name__ == '__main__':
	douyu = DouyuSpider()
	douyu.run()