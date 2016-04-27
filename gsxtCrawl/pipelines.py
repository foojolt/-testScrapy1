# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time

class GsxtcrawlPipeline(object):


    def __init__(self):
        timeStr = time.strftime("%m%d-%H%M%S-") 
        listHttpFile = timeStr + "list-http.dat"
        singleHttpFile = timeStr + "single-http.dat"
        singleInfoFile = timeStr + "single-info.dat"

        httpHeaders = ["taskType","region","params","url","status","headers","body",]
        infoHeaders = ["taskType","region","name","props",]
        
        listHttpCsv = csv.DictWriter( open( listHttpFile, 'w' ), httpHeaders )
        singleHttpCsv = csv.DictWriter( open( singleHttpFile, 'w' ), httpHeaders )
        singleInfoCsv = csv.DictWriter( open( singleInfoFile, 'w' ), infoHeaders)

        self.csvWriters = { "listHttp": listHttpCsv, "singleHttp": singleHttpCsv, "singleInfo": singleInfoCsv }

    def process_item(self, item, spider):

        writer = self.csvWriters.get( item["taskType"] )
        if writer:
            writer.writerow( dict( item.iteritems() ) )
        return item
