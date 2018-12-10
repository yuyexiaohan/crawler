# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re


class CrawlspiderPipeline(object):
    def process_item(self, item, spider):
        item["job_content"], item["job_request"] = self.process_content(item["job_content"], item["job_request"])
        self.save_file(item)
        # print("item:", item)
        return item

    def save_file(self, item):
        """存储爬去文件"""
        file_path = "./tencent_hr.txt"
        with open (file_path, "a", encoding="utf-8") as f:
            f.write (json.dumps (dict(item), ensure_ascii=False, indent=2))
            f.write ("\n")
        print ("保存成功！")

    def process_content(self, job_content, job_request):
        """处理文档内容"""
        job_content = self.contet_manage(job_content)
        job_request = self.contet_manage(job_request)
        return job_content, job_request

    def contet_manage(self, li):
        li = [re.sub (r"\r|\s+", "", i) for i in li]
        li = [i for i in li if len (i) > 0]
        return li

