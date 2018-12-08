# -*- coding: utf-8 -*-
import scrapy


class HomewhSpider(scrapy.Spider):
    name = 'homewh'
    allowed_domains = ['wuhan.gov.cn']
    start_urls = ['http://wuhan.gov.cn/']

    def parse(self, response):
        pass
