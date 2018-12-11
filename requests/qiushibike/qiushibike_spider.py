# coding=utf-8 
# Time : 2018/12/6
# Author : achjiang
import requests
from lxml import etree
import json

"""
爬去糗百的热门
爬取标题、图片、内容、好笑数、评论数、最佳评论、
"""
class QiubaiSpider():
	"""糗百"""

	def __init__(self, start_pag, totle_num_pag):
		self.start_pag = start_pag
		self.total_num_pag = totle_num_pag
		self.start_url = "https://www.qiushibaike.com/8hr/page/1/"
		self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

	def get_parse(self, url):
		"""获取数据"""
		response = requests.get(url, headers=self.headers)
		return response.content.decode('utf-8')

	def get_content_list(self, html_str):
		"""获取页面数据"""
		html = etree.HTML(html_str)
		div_list = html.xpath("//div[@id='content-left']/div")
		# print('*'*50, div_list, '*'*50)
		content_list = []
		for li in div_list:
			item = {}
			item["author_name"] = li.xpath(".//div[@class='author clearfix']/a/h2/text()")
			item["author_name"] = [i.replace("\n", "") for i in item["author_name"]][0] if len(item["author_name"]) > 0 else None

			item["content"] = li.xpath(".//div[@class='content']/span/text()")
			item["content"] = [i.replace("\n", "") for i in item["content"]] if len(item["content"]) > 0 else None

			item["img"] = li.xpath(".//div[@class='thumb']/a/img/@src")
			item["img"] = item["img"][0] if len(item["img"]) > 0 else None

			item["luck_face"] = li.xpath(".//span[@class='stats-vote']/i/text()")
			item["luck_face"] = item["luck_face"][0] if len(item["luck_face"]) > 0 else None

			item["comment_nums"] = li.xpath(".//span[@class='stats-comments']/a/i/text()")
			item["comment_nums"] = item["comment_nums"][0] if len(item["comment_nums"]) > 0 else None

			item["hot_comment"] = li.xpath(".//div[@class='main-text']/text()")
			item["hot_comment"] = [i.replace("\n", "") for i in item["hot_comment"]] if len(item["hot_comment"]) > 0 else None
			content_list.append(item)
			# print ('-' * 50, item, '-' * 50, '\n')
			# print ('+' * 50, content_list, '+' * 50, '\n')
		return content_list

	def save_content_list(self, content_list):
		"""存储数据"""
		file_path = '糗百热门' + '.txt'
		with open(file_path, 'a', encoding='utf-8') as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write('\n')
		# print("文件保存成功！")

	def run(self):
		"""爬去数据"""
		# 1.获取url
		next_url = self.start_url
		i = self.start_pag
		while i < self.total_num_pag:
			html_str = self.get_parse(next_url)
			# 2.下一页url
			next_url = "https://www.qiushibaike.com/8hr/page/%s/" % (str(i))
			# 3.获取数据
			content_list = self.get_content_list(html_str)
			# 4.存储数据
			self.save_content_list(content_list)
			print("第{}页保存成功！".format(i))
			i += 1


if __name__ == '__main__':
	# 实例化数据
	qb = QiubaiSpider(1, 14)
	qb.run()