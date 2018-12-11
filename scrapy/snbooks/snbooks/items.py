# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnbooksItem(scrapy.Item):
    # define the fields for your item here like:
    cy_title = scrapy.Field()
    cy_href = scrapy.Field()
    book_price = scrapy.Field()
    book_desc = scrapy.Field()
    comment_nums = scrapy.Field()
    book_store = scrapy.Field()
    book_href = scrapy.Field()

