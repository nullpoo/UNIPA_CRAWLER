# -*- coding: utf-8 -*-
#エンコードなどの文字列処理用
import re, unicodedata
#日付関連
from datetime import date

def ScrapeDatetime(_date):
    #2012年07月07日(木曜日)や、7月7日などに対応
    p1 = re.compile(u"^((?P<year>\d{4})年)?(?P<month>\d+)月(?P<day>\d+)日.*")
    #2012/07/07(木)や、7/7などに対応
    p2 = re.compile(u"^((?P<year>\d{4})/)?(?P<month>\d+)/(?P<day>\d+).*")
    #和暦
    p3 = re.compile(u"^(平成)?(?P<year>\d{2})年(?P<month>\d+)月(?P<day>\d+)日.*")
    ################back#################################################
    #2012年07月07日(木曜日)や、7月7日などに対応
    #p1 = re.compile(u"^((?P<year>\d{4})年)?(?P<month>\d+)月(?P<day>\d+)日")
    #2012/07/07(木)や、7/7などに対応
    #p2 = re.compile(u"^((?P<year>\d{4})/)?(?P<month>\d+)/(?P<day>\d+)")
    #和暦
    #p3 = re.compile(u"^(平成)?(?P<year>\d{2})年(?P<month>\d+)月(?P<day>\d+)日")
    #############################################

    if(p1.search(_date) != None):
        _year = int(p1.match(_date).group('year'))
        _month = int(p1.match(_date).group('month'))
        _day = int(p1.match(_date).group('day'))

        if (_year == None):
            _today = date.today()
            _d = date(_today.year, _month, _day)
            if (_d < date(_today.year+1, 1, 1)):
                return str(_d)
            else:
                return str(date(_today.year+1, _month, _day))
        else:
            return str(date(_year, _month, _day))

    elif(p2.search(_date) != None):
        _year = p2.match(_date).group('year')
        _month = p2.match(_date).group('month')
        _day = p2.match(_date).group('day')
        _today = date.today()
        if(_year == None):
            _d = date(_today.year, int(_month), int(_day))
            if (_d < date(_today.year+1, 1,1)):
                return str(_d)
            else:
                return str(date(_today.year+1, _month, _day))
        else:
            return str(date(_today.year, _month, _day))
    elif(p3.search(_date) != None):
        _year = p3.match(_date).group('year')+1988
        _month = p3.match(_date).group('month')
        _day = p3.match(_date).group('day')

        if(_year == None):
            _today = date.today()
            _d = date(_today.year, _month, _day)
            if (_d < date(_today.year+1, 1,1)):
                return str(_d)
            else:
                return str(date(_today.year+1, _month, _day))
        else:
            return str(date(_today.year, _month, _day))
    else:
        return str(date(2001,1,1))
