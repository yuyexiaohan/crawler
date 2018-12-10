# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']  # 当前起始页

    rules = (
        # url规则，
        # LinkExtractor：链接提取器，
        # allow：允许爬去的url,按照实际网页情况填写，框架回自动补全
        # callback: 调用具体的函数执行，该url界面的信息提取
        # follow：是否跟随循环
        # 1.详情页面：
        Rule (LinkExtractor (allow=r'position_detail\.php\?id=\d+&keywords=&tid=\d&lid=\d'), callback='parse_item'),
        # 2.翻页部分
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
        # print(item)
        return item




