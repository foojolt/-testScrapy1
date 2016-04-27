# -*- coding: utf-8 -*-

import scrapy

class HttpItem(scrapy.Item):
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

