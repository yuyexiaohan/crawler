# coding=utf-8 
# Time : 2018/12/6
# Author : achjiang
from lxml import etree
import requests
import json


class BaiduTiebaSpider(object):
	"""贴吧爬虫"""

	def __init__(self, tb_name):
		self.tb_name = tb_name
		self.start_url = "https://tieba.baidu.com/mo/q/m?word=" + tb_name + "&tn4=bdKSW&sub4=&pn=0&"
		self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 \
		(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
		self.part_url = "https://tieba.baidu.com"

	def parse_url(self, url):
		"""获取界面响应"""
		print(url)
		response = requests.get(url, headers=self.headers)
		return response.content.decode('utf-8')

	def get_content_list(self, html_str):
		"""获取数据"""
		html = etree.HTML(html_str)  # 获得HTML文件
		print('*'*100, html, '-'*100)
		div_list = html.xpath("//li[@class='tl_shadow tl_shadow_new']")
		print('*' * 100, div_list, '-' * 100)
		content_list = []
		for li in div_list:
			item = dict({})
			item["title"] = li.xpath("//ul[@id='frslistcontent']//div[@class='ti_title']/span/text()")[0]\
				if len(li.xpath("//ul[@id='frslistcontent']//div[@class='ti_title']/span/text()")[0]) > 0 else None
			item["href"] = self.part_url + li.xpath("//ul[@id='frslistcontent']//a/@href")[0]\
				if len(li.xpath("//ul[@id='frslistcontent']//a/@href")[0]) else None
			item["img_list"] = self.get_img_list(item["href"], [])
			item["img_list"] = [requests.utils.unquote(i).split("src=")[-1] for i in item["img_list"]]
			content_list.append(item)
		current_pag = html.xpath("//input/@value")
		print('*' * 100, current_pag, '-' * 100)
		# 提取下一页的url地址
		next_url = self.part_url + html.xpath("//a[text()='下一页']/@href")[0] if len(
			html.xpath("//a[text()='下一页']/@href")) > 0 else None
		return content_list, next_url

	def get_img_list(self, detail_url, total_img_list):
		"""获取帖子图片"""
		# 3.2请求列表页的url地址，获取详情页的第一页
		detail_html_str = self.parse_url(detail_url)
		detail_html = etree.HTML(detail_html_str)
		# 3.3提取详情页第一页的图片，提取下一页的地址
		img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
		total_img_list.extend(img_list)
		# 3.4请求详情页下一页的地址，进入循环3.2-3.4
		detail_next_url = detail_html.xpath("//a[text()='下一页']/@href")
		if len(detail_next_url) > 0:
			detail_next_url = self.part_url + detail_next_url[0]
			return self.get_img_list(detail_next_url, total_img_list)

		return total_img_list

	def save_content_list(self, content_list):
		"""保存数据"""
		file_path = self.tb_name + ".txt"
		with open(file_path, "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")
		print("保存成功")

	def run(self):  # 实现主要逻辑
		next_url = self.start_url
		while next_url is not None:
			# 1.start_url
			# 2.发送请求，获取响应
			html_str = self.parse_url(next_url)
			# print('html_str:', html_str)
			# 3.提取数据，提取下一页的url地址
			# 3.1提取列表页的url地址和标题
			# 3.2请求列表页的url地址，获取详情页的第一页
			# 3.3提取详情页第一页的图片，提取下一页的地址
			# 3.4请求详情页下一页的地址，进入循环3.2-3.4
			# content_list, next_url = self.get_content_list(html_str)
			content_list = self.get_content_list(html_str)
			# 4.保存数据
			self.save_content_list(content_list)
			# 5.请求下一页的url地址，进入循环2-5不


if __name__ == '__main__':
	tieba = BaiduTiebaSpider('弹珠')
	tieba.run()
