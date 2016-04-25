# -*- coding: utf-8 -*-
import scrapy


class ListSpider(scrapy.Spider):
    name = "list"
    allowed_domains = ["www.baidu.com"]
    start_urls = (
        'http://www.baidu.com/',
    )

    def parse(self, response):
        pass
