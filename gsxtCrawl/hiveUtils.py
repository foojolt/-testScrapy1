# -*- coding: utf-8 -*-

import re

_colSep = ','
_itemSep = '/'
_keySep = ':'


def _escape( value ):
    if not value:
        return ""

    if type(value) is not str and type(value) is not unicode:
        return str(value)

    n = re.sub( _itemSep, ur"\\／", value )
    n = re.sub( _keySep, ur"\\：", n )
    n = re.sub( r"[\r\n]+", r"\\n", n )
    n = re.sub( _colSep, r"\\，", n )
    return n

def toHiveMap( m ):
    return _itemSep.join( [ k + _keySep + _escape(m[k]) for k in m ] )

def toHiveRow(arr):
    newArr = [ toHiveMap( m ) if type(m) is dict else _escape( m ) for m in arr ]
    return _colSep.join( newArr )
