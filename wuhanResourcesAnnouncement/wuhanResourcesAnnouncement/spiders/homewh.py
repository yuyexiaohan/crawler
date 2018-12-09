# -*- coding: utf-8 -*-
import scrapy
from wuhanResourcesAnnouncement.items import WuhanresourcesannouncementItem
import re


"""
爬去武汉市民之家公布的资源公告，列表及详情页情况
'http://home.wuhan.gov.cn/zyjygg/index.jhtml'
"""


class HomewhSpider(scrapy.Spider):
    name = 'homewh'
    allowed_domains = ['wuhan.gov.cn']
    start_urls = ['http://home.wuhan.gov.cn/zyjygg/index.jhtml']

    def parse(self, response):
        """爬去资源交易公告"""
        content_list = response.xpath("//div[@class='news_list']/ul/li")
        for li in content_list:
            item = WuhanresourcesannouncementItem()
            item["title"] = li.xpath("./a/text()").extract_first()
            item["href"] = li.xpath("./a/@href").extract_first()
            item["pub_date"] = li.xpath("./span/text()").extract_first()
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta = {"item": item}
            )

        # next_url = str(response.xpath("//a[text()='下一页']/@onclick").split("="))[1]
        next_url_part = response.xpath("//a[text()='下一页']/@onclick").extract()
        print ("next_url_part:", next_url_part)
        if len(next_url_part) > 0:
            next_url_part = response.xpath ("//a[text()='下一页']/@onclick").extract ()[0]
            next_url_part = re.findall (r"index_[0-9]+\.jhtml", next_url_part)[0]
            next_url = "http://home.wuhan.gov.cn/zyjygg/" + next_url_part

            yield scrapy.Request(
                next_url,
                callback=self.parse
            )


    def parse_detail(self, response):
        """详情页内容处理"""
        item = response.meta["item"]
        item["content"] = response.xpath ("//div[@class='news_cont']/text()").extract()
        item["pv"] = response.xpath ("//div[@class='miaosu']/text()").extract()
        yield item


