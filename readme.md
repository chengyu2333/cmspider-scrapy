## 爬虫说明

用于爬取新闻的通用爬虫，使用MongoDB作为数据仓库。

## 使用说明

爬取列表页

`scrapy crawl cms_list`

爬取新闻页

`scrapy crawl cms_article`

## 配置说明
settings.py
```
# MongoDB数据库配置
MONGODB_HOST = "192.168.1.34"
MONGODB_PORT = 27017
MONGODB_DBNAME = "cmspider"
```
cms_config.py
```
# 入口新闻列表页url
start_url = ["http://news.hexun.com/original/"]
# 列表的a标签的选择器
href_xpath = '//*[@id="temp01"]/ul/li/a'
# "下一页"按钮的选择器
next_page_css = ".next"
```
