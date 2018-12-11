# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy


class DdbookSpider(RedisSpider):
    name = 'ddbook'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        bc_list = response.xpath("//div[@class='con flq_body']/div")
        for bc in bc_list:
            item = {}
            item["category"] = bc.xpath("./dl/dt//text()").extract()
            item["category"] = [i.strip() for i in item["category"] if len(item["category"]) > 0]
            dl_list = bc.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item["dt_category"] = dl.xpath("./dt/text()").extract()
                item["dt_category"] = [i.strip() for i in item["dt_category"] if len (item["dt_category"]) > 0]
                category_list = dl.xpath("./dd/a")
                for li in category_list:
                    item["book_catagory"] = li.xpath("./span/text()").extract_first()
                    item["category_href"] = li.xpath("./@href").extract_first()
                    print(item["category"])
                    yield item
                    # if item["category_href"] is not None:
                        # yield scrapy.Request(item["category_href"],
                        #                      callback=self.parse_book_list,
                        #                      meta={"item": deepcopy(item)})

    # def parse_book_list(self, response):
    #     """书本分类列表页处理"""
    #     item = response.meta["item"]
    #     book_list = response.xpath("")




