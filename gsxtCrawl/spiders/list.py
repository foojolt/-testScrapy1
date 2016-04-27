# -*- coding: utf-8 -*-

import scrapy
from gsxtCrawl import fromCurlIterator, fromCurlSingle
from gsxtCrawl import loadListTasks
from gsxtCrawl.items import HttpItem, SingleExtractItem
import pdb
import logging
import sys
import json

class ListSpider(scrapy.Spider):

    name = "list"

    def start_requests(self):
        tasks = loadListTasks( self.taskFile if hasattr( self, "taskFile" ) else "taskFile" )
        for task in tasks:
            if hasattr( self, "region" ) and self.region != task["region"]:
                logging.debug( "skip region: %s", task )
                continue
            for req in fromCurlIterator( task["listCompanyCurlTemplate"], 
                            task["listParameters"], { "task": task } ):
                req.callback  = self.parseList
                yield req

    def parseList( self, response ):
        reqOrItems = []
        yield self.createListItem( response )

        task = response.meta["task"]
        body = response.body
        allMatches = task["listExtractRegex"].finditer( body )
        for singleCompany in allMatches:
            params = singleCompany.groupdict()
            logging.debug("found company info: %s", params)
            curlCmd = task["singleCompanyCurlTemplate"].format( ** params )
            req = fromCurlSingle( curlCmd, { "task": task, "params": params } )
            req.callback = self.parseSingle
            yield req

    def createListItem(self, response):
        item = HttpItem()
        item["region"] = response.meta["task"]["region"]
        item["params"] = str(response.meta["params"])
        item["taskType"] = "listHttp"
        item["url"] = response.url
        item["status"] = response.status
        item["headers"] = response.headers
        item["body"] = response.body
        return item

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
        extractItem["props"] = json.dumps(props, ensure_ascii=False)
        yield extractItem



