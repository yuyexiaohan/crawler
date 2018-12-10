# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class SnbooksPipeline(object):
    def process_item(self, item, spider):
        self.save_file(item)
        # print("item:", item)
        return item

    def save_file(self, item):
        """存储爬去文件"""
        file_path = "./snbooks.text"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(dict(item), ensure_ascii=False, indent=2))
            f.write("\n")
        print("保存成功！")
