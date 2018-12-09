# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
# from wuhanResourcesAnnouncement.settings import MONGO_HOST


class WuhanresourcesannouncementPipeline(object):
    def process_item(self, item, spider):
        # spider.settings.get("MONGO_HOST")
        item["content"], item["pv"] = self.process_content(item["content"], item["pv"])
        file_path = "./home_wh.txt"
        with open (file_path, "a", encoding="utf-8") as f:
            f.write (json.dumps(dict(item), ensure_ascii=False, indent=2))
            f.write ("\n")
        print ("保存成功！")
        # print(item)
        return item

    def process_content(self, content, pv):
        """对详情内容进行处理"""
        content = [re.sub(r"\r|\n|\t|\xa0", "", i) for i in content]
        content = [i for i in content if len(i) > 0]
        if len(pv) > 0:
            pv = [re.sub(r"\r|\n|\t|\xa0", "", i) for i in pv]
            pv = [i for i in pv if len(i) > 0]
            pv = pv[0].split("浏览次数：")[1]

        return content, pv
