# -*- coding: utf-8 -*-
import scrapy
# from snbooks.items import SnbooksItem
from copy import deepcopy

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
            print("item['cy_href']:", item["cy_href"])
            yield scrapy.Request(
                item["cy_href"],
                callback=self.parse_list,
                meta={"item": deepcopy(item)}
            )

    def parse_list(self, response):
        """分类详情列表"""
        print("---"*50)
        item = deepcopy(response.meta["item"])
        book_list = response.xpath("//div[@id='filter-results']/ul/li")
        for book in book_list:
            item["book_price"] = book.xpath(".//div[@class='res-info']/p/em/text()").extract_first()
            item["book_desc"] = book.xpath(".//div[@class='res-info']/p[2]/a/text()").extract_first()
            item["img_src"] = book.xpath(".//img/@src").extract_first()
            item["comment_nums"] = book.xpath(".//div[@class='res-info']/p[3]/a[1]/text()").extract_first()
            item["book_store"] = book.xpath(".//div[@class='res-info']/p[4]/a/text()").extract_first()
            item["book_href"] = book.xpath(".//div[@class='res-info']/p[2]/a/@href").extract_first()
            print ("item:", item)
            yield item
        next_url_part = response.xpath("//a[@id='nextPage']/@href").extract_first()
        print("***"*50, next_url_part, "***"*50)
        if next_url_part is not None:
            next_url = "https://list.suning.com" + next_url_part
            print("next_url:", next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_list,
	            meta={"item": response.meta["item"]}
            )