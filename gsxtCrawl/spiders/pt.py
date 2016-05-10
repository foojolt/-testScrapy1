# -*- coding: utf-8 -*-

import scrapy
from gsxtCrawl import fromCurlIterator, fromCurlSingle
from gsxtCrawl import loadListTasks
from gsxtCrawl.items import HttpItem, SingleExtractItem
import pdb
import logging
import sys
import json
import time
import re

logger = logging.getLogger(__name__)

class PatternSpider(scrapy.Spider):

    name = "pt"

    def start_requests(self):
        
        src = "shanghai-list-http.dat" # source file
        ext = re.compile( r"view[?]uuid=(?P<uuid>[^&]+)" ) # extract info
        curl = "curl 'https://www.sgs.gov.cn/notice/notice/view?uuid={uuid}&tab=01' -H 'Host: www.sgs.gov.cn' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://www.sgs.gov.cn/notice/search/ent_spot_check_list' -H 'Cookie: JSESSIONID=0000P0jNyfahLmaWCLagXXCeHrZ:19307hbmg' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0'"
        task = { "region":"shanghai", "singleExtractRegex":  map( lambda it: re.compile( it ), "名称</th>[^<]*<td>(?P<name>[^<]+)</td>.*<-ps->类型</th>[^<]*<td>(?P<companyType>[^<]+)</td>.*<-ps->注册资本</th>[^<]*<td>(?P<registerCapital>[^<]+)</td>.*<-ps->成立日期</th>[^<]*<td>(?P<openDate>[^<]+)</td>.*<-ps->住所</th>[^<]*<td>(?P<location>[^<]+).*<-ps->经营范围</th>[^<]*<td[^>]*>(?P<businessScope>[^<]+).*".split( "<-ps->" ) ) }
        with open(src) as file:
            for line in file:
                am = ext.finditer( line )
                for m in am:
                    params = m.groupdict()
                    req = fromCurlSingle( curl.format( ** params ), { "task": task, "params": params }, 100 )
                    req.callback = self.parseSingle
                    yield req


    def parseSingle( self, response ):
        httpItem = HttpItem()
        httpItem["region"] = response.meta["task"]["region"]
        httpItem["params"] = str(response.meta["params"])
        httpItem["taskType"] = "singleHttp"
        httpItem["url"] = response.url
        httpItem["status"] = response.status
        httpItem["headers"] = response.headers
        httpItem["body"] = response.body
        yield httpItem

        task = response.meta["task"]
        body = response.body.decode("utf8")
        regexArr = task["singleExtractRegex"]
        
        # pdb.set_trace()
        if not body:
            return

        props = {}
        for mat in map( lambda regex: regex.search( body ),  regexArr):
            if mat:
                props.update( mat.groupdict() )
        props = { k : props[k].decode( "utf8" ) if props[k] else props[k] for k in props }
        
        if "name" not in props:
            return
            
        name = props.pop("name")
        region = task["region"]
        extractItem = SingleExtractItem()
        extractItem["taskType"] = "singleInfo"
        extractItem["name"] = name
        extractItem["region"] = region
        extractItem["props"] = props
        yield extractItem



