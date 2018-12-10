# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Tencent1Spider(CrawlSpider):
    name = 'tencent1'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    rules = (
        Rule (LinkExtractor (allow=r'position\.php\?&start=\d+#a'), follow=True),
    )

    def parse_item(self, response):
        """列表页信息爬取"""
        tr_list = response.xpath ("//table[@class='tablelist']//tr")[1:-1]
        for tr in tr_list:
            item = {}
            item["tag"] = "tencent1"
            item["title"] = tr.xpath (".//td[1]/a/text()").extract_first ()
            item["category"] = tr.xpath ("./td[2]/text()").extract_first ()
            item["nums"] = tr.xpath (".//td[3]/text()").extract_first ()
            item["position"] = tr.xpath (".//td[4]/text()").extract_first ()
            item["publish_date"] = tr.xpath (".//td[5]/text()").extract_first ()
            item["detail_href"] = "https://hr.tencent.com/" + tr.xpath (".//td[1]/a/@href").extract_first ()
            yield scrapy.Request(
                item["detail_href"],
                callback=self.parse_detail,
                meta={"item": item})

    def parse_detail(self, response):
        """详情页信息存储"""
        item = response.meta["item"]
        item["job_content"] = response.xpath ("//table[@class='tablelist textl']//tr[3]//text()").extract ()
        item["job_require"] = response.xpath ("//table[@class='tablelist textl']//tr[4]//text()").extract ()
        yield item