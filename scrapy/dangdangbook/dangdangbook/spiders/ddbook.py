# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import urllib


class DdbookSpider(RedisSpider):
    name = 'ddbook'
    allowed_domains = ['dangdang.com']
    # 当使用redisspider时，不需要start_url
    # start_urls = ['http://book.dangdang.com/']
    # 使用redis_key时，当再文件目录运行`scrapy crawl ddbook`之后，需要
    # 在redis数据库命令行中输入`lpush dangdang http://book.dangdang.com/`命令，系统才开始爬取数据
    redis_key = "ddbook"

    def parse(self, response):
        bc_list = response.xpath("//div[@class='con flq_body']/div")
        for bc in bc_list:
            item = {}
            item["category"] = bc.xpath("./dl/dt//text()").extract()
            item["category"] = [i.strip() for i in item["category"] if len(item["category"]) > 0]
            dl_list = bc.xpath(".//dl[@class='inner_dl']")
            for dl in dl_list:
                item["dt_category"] = dl.xpath("./dt/text()").extract()
                item["dt_category"] = [i.strip() for i in item["dt_category"] if len (i.strip()) > 0][0]
                category_list = dl.xpath("./dd/a")
                for li in category_list:
                    item["book_catagory"] = li.xpath("./span/text()").extract_first()
                    item["category_href"] = li.xpath("./@href").extract_first()
                    # print("*"*20)
                    print(item, item["category"])
                    if item["category_href"] is not None:
                        yield scrapy.Request(item["category_href"],
                                             callback=self.parse_book_list,
                                             meta={"item": deepcopy(item)})

    def parse_book_list(self, response):
        """书本分类列表页处理"""
        item = response.meta["item"]
        book_list = response.xpath("//div[@id='search_nature_rg']/ul/li")
        for li in book_list:
            item["book_title"] = li.xpath("./p[1]/a/text()").extract_first()
            item["book_img"] = li.xpath(".a/img/@src").extract_first()
            item["book_desc"] = li.xpath("./p[2]").extract()
            item["book_price"] = li.xpath("./p[3]/span/text()").extract_first().split("￥")[1]
            item["book_author"] = li.xpath("./p[5]/span[1]/a/text()").extract()
            item["book_pub"] = li.xpath("./p[5]/span[2]/a/text()").extract_first()
            item["book_pub_time"] = li.xpath("./p[5]/span[2]/text()").extract_first().split("/")[1]
            print(item)
            yield item

        next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": item}
                )
