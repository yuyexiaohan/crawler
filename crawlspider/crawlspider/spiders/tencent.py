# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    rules = (
        Rule (LinkExtractor (allow=r'position_detail\.php\?id=\d+&keywords=&tid=\d&lid=\d'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'), follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath ("//table[@class='tablelist textl']//td[@id='sharetitle']/text()").extract_first()
        item["category"] = response.xpath ("//table[@class='tablelist textl']//tr[2]/td[2]/text()").extract_first()
        item["nums"] = response.xpath ("//table[@class='tablelist textl']//tr[2]/td[3]/text()").extract_first()
        item["position"] = response.xpath ("//table[@class='tablelist textl']//tr[2]/td[1]/text()").extract_first()
        # item["publish_date"] = response.xpath ("./td[5]/text()").extract_first()
        item["job_content"] = response.xpath ("//table[@class='tablelist textl']//tr[3]//text()").extract()
        item["job_request"] = response.xpath ("//table[@class='tablelist textl']//tr[4]//text()").extract()
        print(item)
        return item




