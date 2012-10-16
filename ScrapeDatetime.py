# -*- coding: utf-8 -*-
#エンコードなどの文字列処理用
import re, unicodedata
#日付関連
import time
import datetime
import dateutil.parser

_date = u'2012年7月19日（木）'

def ScrapeDatetime(_date):
    #2012年07月07日(木曜日)や、7月7日などに対応
    p1 = re.compile(u"^(\d+年)?\d+月\d+日")
    #2012/07/07(木)や、7/7などに対応
    p2 = re.compile(u"^(\d+/)?\d+/\d+")

    if(p1.search(_date) != None):
        _date = p1.match(_date).group()
        _date = _date.replace(u'年','-').replace(u'月','-').replace(u'日','')
        return str(dateutil.parser.parse(_date))
    elif(p2.search(_date) != None):
        _date = p2.match(_date).group()
        if(re.search(u"^\d+/\d+/\d+",_date) != None):
            return str(dateutil.parser.parse(_date))
        else:
            _date = '2012/'+_date
            return str(dateutil.parser.parse(_date))
    else:
        return u'2001-01-01'
