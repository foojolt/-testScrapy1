# -*- coding: utf-8 -*-

from scrapy import Request
import json
import re
import shlex
import argparse


def _createCurlCmdParser():
    parser = argparse.ArgumentParser(description='internal curl cmdline parser')
    parser.add_argument( "-H", action="append", dest="headers" )
    parser.add_argument( "--data", action="store", dest="data" )
    parser.add_argument( "--compressed", action="store_true", dest="compressed" )
    return parser

_curlArgParser = _createCurlCmdParser()

def fromCurlSingle( curlCmd, meta ):
    argv = shlex.split( curlCmd )
    cmdOpts = _curlArgParser.parse_args( argv[2:] )
    headers = {}
    for headStr in cmdOpts.headers:
        headers[ headStr[0:headStr.index(":")] ] = headStr[ headStr.index(":")+1:]
    url = argv[1]
    if cmdOpts.data:
        return Request( url, method="POST", headers = headers, body = cmdOpts.data, meta = meta )
    else:
        return Request( url, headers = headers, meta = meta )

def fromCurlIterator( curlCmdTemplate, paramsIterator, meta ):
    for params in paramsIterator:
        curlCmd = curlCmdTemplate.format( **params )
        meta["params"] = params
        yield fromCurlSingle(curlCmd, meta)

def pageIter( minPage, maxPage ):
    for page in xrange( minPage, maxPage+1 ):
        yield {"page": page}

def loadListTasks(taskFile):
    with open(taskFile, "r") as f:
        for line in f:
            #region, 
            #listCompanyCurlTemplate, listParameters { maxPage: xxx }, listExtractRegex, 
            #singleCompanyCurlTemplate, singleExtractRegex
            task = json.loads( line )
            #page iterator
            lp = task["listParameters"]
            task["listParameters"] = pageIter( lp.get("minPage") or 1, lp["maxPage"] )
            #pre check
            
            task["listExtractRegex"] = re.compile( task["listExtractRegex"], re.M | re.DOTALL )
            task["singleExtractRegex"] = [ re.compile( pt, re.M | re.DOTALL ) for pt in 
                                            task["singleExtractRegex"].split( "<-ps->" )]
            yield task
            


    