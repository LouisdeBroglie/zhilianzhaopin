# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymongo
import jieba
import pandas as pd

from zhilian import data_deal


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONG_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db['zhilian'].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.results = self.db['zhilian'].find({'requirement': {'$exists': True}})
        self.requirement = ''
        for self.result in self.results:
            self.requirement = self.requirement + str(self.result['requirement'])
        data_deal.Frequency(self.requirement)
        self.client.close()

