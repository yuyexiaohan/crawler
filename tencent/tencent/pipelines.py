# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
数据库代码，存储到数据库
"""
"""
存储到文件tencent_hr.txt
"""
import json
from tencent.items import TencentItem


class TencentPipeline(object):
    def process_item(self, item, spider):
        # 在多个爬虫的情况下，判断item对象是来自于那个爬虫，
        # 并做进一步的处理
        if isinstance(item, TencentItem):
            file_path = "./tencent_hr.txt"
            with open (file_path, "a", encoding="utf-8") as f:
                f.write (json.dumps(item, ensure_ascii=False, indent=2))
                f.write ("\n")
            print("保存成功！")
            print("item:", item)
        return item
