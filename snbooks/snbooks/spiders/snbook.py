# -*- coding: utf-8 -*-
import scrapy


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.comm']
    start_urls = ['http://suning.comm/']

    def parse(self, response):
        pass
