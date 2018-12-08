# -*- coding: utf-8 -*-
import scrapy


class TencrntHrSpider(scrapy.Spider):
    name = 'tencrnt_hr'
    allowed_domains = ['tencent.com']
    start_urls = ['http://tencent.com/']

    def parse(self, response):
        pass
