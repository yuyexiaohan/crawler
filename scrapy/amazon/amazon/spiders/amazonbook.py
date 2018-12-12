# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule  # CrawlSpider 去重爬虫模块
from scrapy_redis.spiders import RedisCrawlSpider  # 分布式去重爬虫模块
import re


class AmazonbookSpider(RedisCrawlSpider):
    """继承RedisCrawlSpider 分布式爬虫"""
    name = 'amazonbook'
    allowed_domains = ['amazon.cn']
    # start_urls = ['http://amazon.cn/']
    redis_key = 'amazonbook'

    rules = (
        # 各书籍分类的列表
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='leftNav']//ul[1]/ul//li",)), follow=True),
        # 详情页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..",)), callback="parse_book_detail"),
        # 翻页
        Rule(LinkExtractor(restrict_xpaths=("//a[@title='下一页']",)), follow=True),
    )

    def parse_book_detail(self, response):
        item = {}
        item["title"] = response.xpath("//span[@id='productTitle']/text()").extract_first()
        if item["title"] is None:
            item["title"] = response.xpath("//span[@id='ebooksProductTitle']/text()").extract_first()
        item["boook_type1"] = response.xpath("//span[@class='a-color-base']/../span/text()").extract_first()
        item["price1"] = response.xpath("//span[@class='a-color-base']/span/text()").extract_first()
        item["boook_type2"] = response.xpath ("//span[@class='a-color-secondary']/../span/text()").extract_first ()
        if item is not None:
            item["price2"] = response.xpath ("//span[@class='a-color-secondary']/span/text()").extract_first ()
        item["pub_date"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first()
        # item["price"] = [re.findall(r'\￥([0-9]+\.[0-9]+)', i) for i in item["price"]]
        item["author"] = response.xpath("//div[@id='bylineInfo']//a/text()").extract()
        # item["img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
        print("item:", item)
        return item
    # rules = (
    #     #匹配大分类的url地址和小分类的url
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@class='categoryRefinementsSection']/ul/li",)), follow=True),
    #     #匹配图书的url地址
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..",)),callback="parse_book_detail"),
    #     #列表页翻页
    #     Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)),follow=True),
    #
    # )
    #
    # def parse_book_detail(self,response):
    #     # with open(response.url.split("/")[-1]+".html","w",encoding="utf-8") as f:
    #     #     f.write(response.body.decode())
    #     item = {}
    #     item["book_title"] = response.xpath("//span[@id='productTitle']/text()").extract_first()
    #     item["book_publish_date"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first()
    #     item["book_author"] = response.xpath("//div[@id='byline']/span/a/text()").extract()
    #     # item["book_img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
    #     item["book_price"] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()").extract_first()
    #     item["book_cate"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li[not(@class)]/span/a/text()").extract()
    #     item["book_cate"] = [i.strip() for i in item["book_cate"]]
    #     item["book_url"] = response.url
    #     item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
    #     # item["book_desc"] = re.findall(r'<noscript>.*?<div>(.*?)</div>.*?</noscript>',response.body.decode(),re.S)
    #     # item["book_desc"] = response.xpath("//noscript/div/text()").extract()
    #     # item["book_desc"] = [i.strip() for i in item["book_desc"] if len(i.strip())>0 and i!='海报：']
    #     # item["book_desc"] = item["book_desc"][0].split("<br>",1)[0] if len(item["book_desc"])>0 else None
    #     print(item)

