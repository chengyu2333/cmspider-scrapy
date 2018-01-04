## 爬虫说明

用于爬取新闻的通用爬虫，使用MongoDB作为数据仓库。

## 使用说明

- 爬取列表页

    `scrapy crawl cms_list`

- 爬取新闻页

    `scrapy crawl cms_article`

- 更换浏览器引擎

    为方便观察调试，默认使用的Chrome浏览器，需要安装chrome driver。
    
    若想使用PhantomJS或其他浏览器可以修改cms_list.py中的get_driver方法。



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
