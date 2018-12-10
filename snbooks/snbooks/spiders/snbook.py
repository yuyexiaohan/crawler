# -*- coding: utf-8 -*-
import scrapy
# from snbooks.items import SnbooksItem
from copy import deepcopy
import re


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        books_category_list = response.xpath("//div[@class='submenu-left']/ul/li")
        # print("books_category_list:", books_category_list)
        for cy_list in books_category_list:
            # item = SnbooksItem()
            item = {}
            item["cy_title"] = cy_list.xpath(".//a/text()").extract_first()
            item["cy_href"] = cy_list.xpath(".//a/@href").extract_first()
            # print("item['cy_href']:", item["cy_href"])
            yield scrapy.Request(
                item["cy_href"],
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_list(self, response):
        """分类详情列表"""
        print("---"*20)
        item = deepcopy(response.meta["item"])
        book_list = response.xpath("//div[@id='filter-results']/ul/li")
        for book in book_list:
            item["book_price"] = book.xpath(".//div[@class='res-info']/p/em/text()").extract_first()  # 价格是Ajax请求获取的，这里暂时存在bug,未修复
            item["book_desc"] = book.xpath(".//div[@class='res-info']/p[2]/a/text()").extract_first()
            item["img_src"] = book.xpath(".//img/@src2").extract_first()
            item["comment_nums"] = book.xpath(".//div[@class='res-info']/p[3]/a[1]/text()").extract_first()
            item["book_store"] = book.xpath(".//div[@class='res-info']/p[4]/a/text()").extract_first()
            item["book_href"] = book.xpath(".//div[@class='res-info']/p[2]/a/@href").extract_first()
            # print ("item:", item)
            yield item
        try:
            current_page = int((re.findall(r"""param.currentPage = "(.*?)";""", response.body.decode())[0]))
            page_numbers = int((re.findall(r"""param.pageNumbers = "(.*?)";""", response.body.decode())[0]))
        except Exception as e:
            print("error:", e)
        else:
            if current_page < page_numbers:
                next_url_part = re.findall(r'^https.*-', item["cy_href"])[0]
                next_url = next_url_part + str(current_page+1) + '.html'
                print("next_url:", next_url)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_list,
                    meta={"item": response.meta["item"]}
                )