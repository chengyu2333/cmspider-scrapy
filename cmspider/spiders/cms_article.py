import scrapy
import time
from .. import items
from .. import settings
from pymongo import MongoClient


class CmsArticleSpider(scrapy.Spider):
    name = "cms_article"

    def __init__(self):
        super(CmsArticleSpider, self).__init__()
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.col_url = self.db["urls"]
        self.source = None

    def start_requests(self):

        urls = self.col_url.find({"$or": [{"status": {"$exists": False}}, {"status": 0}]}).limit(100)
        for url in urls:
            print(url)
            self.source = url['source']
            yield scrapy.Request(url['href'], callback=self.parse)


    def parse(self, response):
        item = items.CmsSourceItem()
        item['source'] = self.source
        item['url'] = response.url
        item['title'] = response.xpath("//title/text()").extract()[0]
        item['html'] = response.text
        item['time'] = time.time()
        yield item

    def close(spider, reason):
        spider.client.close()
