# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GsxtcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HttpItem(scrapy.Item):
    # define the fields for your item here like:
    taskType = scrapy.Field()
    region = scrapy.Field()
    params = scrapy.Field()
    url  = scrapy.Field()
    status = scrapy.Field()
    headers = scrapy.Field()
    body = scrapy.Field()

class SingleExtractItem(scrapy.Item):
    taskType = scrapy.Field()
    region = scrapy.Field()
    name = scrapy.Field()
    props = scrapy.Field()

