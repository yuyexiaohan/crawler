# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        # 函数名称不可变，否则后续调用回报错
        item["hello"] = "world"
        print("MyspiderPipeline")
        return item


class MyspiderPipeline1(object):
    def process_item(self, item, spider):
        # 函数名称不可变，否则后续调用回报错
        print ("MyspiderPipeline1")
        # print(item)
        return item

"""执行结果：
MyspiderPipeline
MyspiderPipeline1
MyspiderPipeline
MyspiderPipeline1

"""
