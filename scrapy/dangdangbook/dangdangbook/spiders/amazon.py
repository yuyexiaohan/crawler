# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['http://amazon.cn/']
    redis_key = 'amazon'

    rules = (
        # 各书籍分类的列表
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='leftNav']//ul[1]/ul//li")), follow=True),
        # 详情页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..")), callback="parse_book_detail"),
        # 翻页
        Rule(LinkExtractor(restrict_xpaths=("//a[@title='下一页']")), follow=True),
    )

    def parse_book_detail(self, response):
        item = {}
        item["title"] = response.xpath("//span[@id='productTitle']/text()").extract_first()
        item["pub_time"] = response.xpath("//h1[@id='title']/span[3]/text()").extract_first()
        item["price"] = response.xpath("//span[@class='a-color-base']/span/text()").extract_first()
        item["author"] = response.xpath("//span[@class='a-color-base']/span/text()").extract()
        item["img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
        print("item:", item)
        return item
