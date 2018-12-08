# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    name = 'itcast'  # 爬虫的名称
    allowed_domains = ['itcast.cn']  # 运行爬去的网站
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']  # start_url

    def parse(self, response):
        """处理start_url响应"""
        # 函数名称不可变，否则后续调用回报错
        # ret1 = response.xpath("//div[@class='tea_con']//h3/text()").extract()  # extract()提取文字
        # print("ret1：", ret1)
        """不加.extract()打印结果：
        ret1： [<Selector xpath="//div[@class='tea_con']//h3/text()" data='朱老师'>, .... <Selector xpath="//div[@class='tea_con']//h3/text()" data='王老师'>]
        # 加.extract()打印结果：
        ['朱老师', ....  '刘老师']
        """

        li_list = response.xpath("//div[@class='tea_con']//li")
        # 这里不能使用之前定义一个content_list,将item通过append方法添加的方式进行，
        # 因为函数（parse）要求返回的必须是个字典，否则报错：
        # Request, BaseItem, dict or None

        for li in li_list:
            item = {}
            item["name"] = li.xpath(".//h3/text()").extract_first()
            item["title"] = li.xpath(".//h4/text()").extract_first()
            # print(item)
            # 变成一个生成器，循环一次得到一个结果，减少内存占用
            # 还需要在settings中开启pipeliness.MyspiderPipeline
            yield item






