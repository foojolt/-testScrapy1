# -*- coding: utf-8 -*-

import time
from gsxtCrawl import toHiveRow

class GsxtcrawlPipeline(object):

    def __init__(self):
        timeStr = time.strftime("%m%d-%H%M%S-")
        listHttpFile = timeStr + "list-http.dat"
        singleHttpFile = timeStr + "single-http.dat"
        singleInfoFile = timeStr + "single-info.dat"

        httpHeaders = ["taskType","region","params","url","status","headers","body",]
        infoHeaders = ["taskType","region","name","props",]
        
        listHttpCsv = open( listHttpFile, 'w' )
        singleHttpCsv = open( singleHttpFile, 'w' )
        singleInfoCsv = open( singleInfoFile, 'w' )

        self.csvWriters = { "listHttp": ( httpHeaders, listHttpCsv ), "singleHttp": ( httpHeaders, singleHttpCsv ), 
                            "singleInfo": ( infoHeaders, singleInfoCsv ) }

    def writerow( self, headers, writer, m ):
        writer.write( toHiveRow( [ m.get(k) for k in headers ] ) )
        writer.write( "\n" )

    def process_item(self, item, spider):
        writer = self.csvWriters.get( item["taskType"] )
        if writer:
            self.writerow( writer[0], writer[1], dict( item.iteritems() ) )
        return item
