# coding=utf-8 
# Time : 2018/12/6
# Author : achjiang
from lxml import etree
import requests
import json


class BaiduTiebaSpider():
	"""贴吧爬虫"""
	def __init__(self, tb_name):
		self.tb_name = tb_name
		self.start_url = "https://tieba.baidu.com/mo/q/m?word=" + tb_name + "&tn4=bdKSW&sub4=&pn=0&"
		self.headers = "{'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}"
		self.part_url = "https://tieba.baidu.com"

	def parse_url(self, url):
		"""获取界面响应"""
		print(url)
		response = requests.get(url, headers=self.headers)
		return response.content

	def get_content_list(self, html_str):
		"""获取数据"""
		html = etree.HTML(html_str) # 获得HTML文件
		div_list = html.xpath("//li[@class='tl_shadow tl_shadow_new']")
		content_list = []
		for li in div_list:
			item= {}
			item["title"] = li.xpath("//div[@class='ti_title']/span/text()")[0] if len(li.xpath("//div[@class='ti_title']/span/text()")[0])>0 else None
			item["href"] = self.part_url + li.xpath("./a/@href")[0] if len(li.xpath("./a/@href")[0]) else None
			item["img_list"] = self.get_img_list(item["href"])

			next_url = html.xpath("//a[@class='j_pager_next bottom_pager_btn pager_next active']").click() if html.xpath("//a[@class='j_pager_next bottom_pager_btn pager_next active']") else None
		return content_list

	def get_img_list(self, detail_url):
		"""获取帖子图片"""
		pass

	def save_content_list(content_list):
		"""保存数据"""
		pass

	def run(self):  # 实现主要逻辑
		next_url = self.start_url
		while next_url is not None:
			# 1.start_url
			# 2.发送请求，获取响应
			html_str = self.parse_url(next_url)
			# 3.提取数据，提取下一页的url地址
			# 3.1提取列表页的url地址和标题
			# 3.2请求列表页的url地址，获取详情页的第一页
			# 3.3提取详情页第一页的图片，提取下一页的地址
			# 3.4请求详情页下一页的地址，进入循环3.2-3.4
			content_list, next_url = self.get_content_list(html_str)
			# 4.保存数据
			self.save_content_list(content_list)
		# 5.请求下一页的url地址，进入循环2-5不