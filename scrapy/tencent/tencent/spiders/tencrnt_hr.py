# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencrntHrSpider(scrapy.Spider):
    name = 'tencrnt_hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            # 方法1：自定义字典存储数据
            # item = {}
            # 方法2：使用scrapy自带的items.py模块进行
            # 这是个类type(item)： <class 'tencent.items.TencentItem'>
            item = TencentItem()
            item["title"] = tr.xpath("./td[1]/a/text()").extract_first()
            item["category"] = tr.xpath("./td[2]/text()").extract_first()
            item["nums"] = tr.xpath("./td[3]/text()").extract_first()
            item["position"] = tr.xpath("./td[4]/text()").extract_first()
            item["publish_date"] = tr.xpath("./td[5]/text()").extract_first()
            yield item

        # 查找下一页地址
        next_url = response.xpath("//a[@id='next']/@href").extract_first()
        if next_url != "javascript:;":
            part_url = "https://hr.tencent.com/"
            next_url = part_url + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )