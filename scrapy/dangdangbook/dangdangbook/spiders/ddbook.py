# -*- coding: utf-8 -*-
import scrapy


class DdbookSpider(scrapy.Spider):
    name = 'ddbook'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']

    def parse(self, response):
        pass
