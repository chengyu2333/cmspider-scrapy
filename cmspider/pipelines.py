# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from . import settings
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError


class CmspiderPipeline(object):

    col_name = "article"

    def process_item(self, item, spider):
        return item


class CmsListPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.urls = self.db["urls"]
        self.article = self.db['article']
        self.urls.ensure_index("href", unique=True)
        self.article.ensure_index("url", unique=True)

    def process_item(self, item, spider):
        if spider.name == "cms_list":
            if item['href'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['href'])
                url = dict(item)
                self.urls.insert(url)
                return item
        elif spider.name == "cms_article":
            if item['url'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['url'])
                article = dict(item)
                try:
                    self.article.insert(article)
                except DuplicateKeyError as dk:
                    pass
                except Exception as e:
                    raise
                self.urls.update({"href": article.get("url")}, {"$set": {"status": 1}})
                return item
        else:
            return item

    def close_spider(self, spider):
        self.client.close()
