# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import pymongo
from pymongo import MongoClient
# client = MongoClient()
# collection = client["yangguang"]["wenzheng"]
from JZ100.items import NewsItem
item = NewsItem()

class Jz100Pipeline(object):
    def process_item(self, item, spider):
        with open('d:\\save.text','a',encoding='utf-8') as f:
            f.write(item)
        return item


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_uri=crawler.settings.get('MONGO_URI')
        )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print('mongdb开启')

    def process_item(self, item, spider):
        # item["content"]=self.process_content(item["content"])

        # print(item)
        self.db[item.collection].insert(dict(item))
        print('数据插入成功')
        return item

    def process_content(self,content):
        content = [re.sub(r"\xa0|\s","",i) for i in content]
        content = [i for i in content if len(i)>0]
        content = "".join(content)
        return content

    def close_spider(self,spider):
        self.client.close()