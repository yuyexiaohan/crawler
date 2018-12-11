# -*- coding: utf-8 -*-
import scrapy
# from snbooks.items import SnbooksItem
from copy import deepcopy
import re


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        """获取元素"""
        # 获取大分类列表
        big_category_list = response.xpath("//div[@class='submenu-left']/p")
        for big_category in big_category_list:
            item = {}
            item["by_title"] = big_category.xpath("./a/text()").extract_first()
            # 获取小分类列表，这里使用同级跟随p标签“following-sibling::”
            category_list = big_category.xpath("./following-sibling::ul[1]/li")
            for li in category_list:
                item["cy_title"] = li.xpath("./a/text()").extract_first()
                item["cy_href"] = li.xpath("./a/@href").extract_first()
                # print("item['cy_href']:", item["cy_href"])
                yield scrapy.Request(
                    item["cy_href"],
                    callback=self.parse_book_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_book_list(self, response):
        """分类详情列表"""
        print("---"*20)
        item = deepcopy(response.meta["item"])
        book_list = response.xpath("//div[@id='filter-results']/ul/li")
        for book in book_list:
            item["book_price"] = book.xpath(".//div[@class='res-info']/p/em/text()").extract_first()  # 价格是Ajax请求获取的，这里暂时存在bug,未修复
            item["book_desc"] = book.xpath(".//div[@class='res-info']/p[2]/a/text()").extract_first()
            item["img_src"] = book.xpath(".//img/@src2").extract_first()
            item["comment_nums"] = book.xpath(".//div[@class='res-info']/p[3]/a[1]/text()").extract_first()
            item["book_store"] = book.xpath(".//div[@class='res-info']/p[4]/a/text()").extract_first()
            item["book_href"] = "https:" + book.xpath(".//div[@class='res-info']/p[2]/a/@href").extract_first()
            print(item["book_href"])
            yield scrapy.Request(item["book_href"],
                                 callback=self.parse_book_detail,
                                 meta={"item": deepcopy(item)})

        # 获取当前页面和分类总页数，如果没有就不翻页
        current_page = re.findall(r"""param.currentPage = "(.*?)";""", response.body.decode())
        page_numbers = re.findall (r"""param.pageNumbers = "(.*?)";""", response.body.decode ())
        if current_page and page_numbers is not None:
            current_page = int(current_page[0])
            page_numbers = int(page_numbers[0])
            if current_page < page_numbers:
                next_url_part = re.findall(r'^https.*-', item["cy_href"])[0]
                next_url = next_url_part + str(current_page+1) + '.html'
                print("next_url:", next_url)
                yield scrapy.Request(
		            next_url,
		            callback=self.parse_book_list,
		            meta={"item": item}
		        )

    def parse_book_detail(self,response):
        """处理详情页内容"""
        item = response.meta["item"]
        # url = "https://product.suning.com/0070088999/104852073.html?safp=d488778a.46602.resultsRblock.10"
        # price_temp_url = "https://pas.suning.com/nspcsale_0_000000000104852073_000000000104852073_0070088999_170_027___.html"
        # 通过返回的js文件数据获取对应的价格，这里通过观察发现js链接的规律，然后通过正则获取js中的价格
        price_temp_url = "https://pas.suning.com/nspcsale_0_000000000{}_000000000{}_{}_170_027_.html"
        p1 = response.url.split("/")[-1].split(".")[0]
        p2 = response.url.split("/")[-2]
        price_url = price_temp_url.format(p1,p1,p2)
        print("price_url：", price_url)
        yield scrapy.Request(
            price_url,
            callback=self.parse_book_pirce,
            meta={"item":item}
        )

    def parse_book_pirce(self,response): #提取图书的价格
        item = response.meta["item"]
        item["book_price"] = re.findall('"netPrice":"(.*?)"',response.body.decode())[0]
        print (item)
        # 返回给pipelines,交给管道符处理
        yield item
