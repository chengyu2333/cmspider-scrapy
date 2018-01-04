import scrapy
import time
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from readability import Document
from retrying import retry
from redis import Redis, ConnectionPool
from . import cms_config
from scrapy.contrib.linkextractors import LinkExtractor
from .. import items


class CmsListSpider(scrapy.Spider):
    name = "cms_list"

    def __init__(self):
        super(CmsListSpider, self).__init__()
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images" : 2}
        chrome_opt.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_opt)
        self.driver.set_page_load_timeout(100)


    def get_driver(self):
        return self.driver

    def get_next_page_css(self):
        return cms_config.next_page_css

    def start_requests(self):
        urls = cms_config.start_url
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lists = response.xpath(cms_config.href_xpath)
        for l in lists:
            url_item = items.CmsListItem()
            url_item['source'] = response.url
            url_item['title'] = Selector(text=l.extract()).xpath("//text()").extract()[0]
            url_item['href'] = Selector(text=l.extract()).xpath("//@href").extract()[0]
            url_item['time'] = time.time()
            print(url_item)
            yield url_item
        yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)

    def close(self, reason):
        pass