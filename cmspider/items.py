# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CmsListItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    time = scrapy.Field()


class CmsSourceItem(scrapy.Item):
    source = scrapy.Field()  # 来源
    url = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    time = scrapy.Field()

