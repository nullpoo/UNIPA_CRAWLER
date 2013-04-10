# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ScrapeContents
# Purpose:
#
# Author:      nullpoo
#
# Created:     08/09/2012
#-------------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
from htmlentity2unicode import htmlentity2unicode
from ScrapeDatetime import ScrapeDatetime
import re

#<br>タグ抜き
def brRemove(contents):
    for b in contents.findAll('br'):
        b.extract()

    return contents

#取得したコンテンツを気合で整形
def ScrapeMainHTML(contents):
    p1 = re.compile(u"^科目名?:?(?P<target>.*)")
    p2 = re.compile(u"^休講日時?:?(?P<target>.*)")
    p3 = re.compile(u"^補講日時?:?(?P<target>.*)")
    p4 = re.compile(u"^日[時付]?:?(?P<target>.*)")
    p5 = re.compile(u"^教員名?:?(?P<target>.*)")
    p6 = re.compile(u"^時限:?(?P<target>.*)")
    p7 = re.compile(u"^補講教室:?(?P<target>.*)")
    p8 = re.compile(u"^備考:?(?P<target>.*)")
    p9 = re.compile(u"^期間?:?(?P<target>.*)")
    dic = {
            u"course":u"",
            u"canceled_date":u"2001-01-01",
            u"revenge_date":u"2001-01-01",
            u"date":u"2001-01-01",
            u"teacher":u"",
            u"time":u"",
            u"revenge_place":u"",
            u"remarks":u"",
            u"term":u"2001-01-01",
    }
    for a in contents:
        pstr = htmlentity2unicode(a.string.replace(' ', '').replace(u'　',''))
        if(p1.search(pstr) != None):
            dic[u"course"] =  p1.search(pstr).group('target')
        elif(p2.search(pstr) != None):
            dic[u"canceled_date"] = ScrapeDatetime(p2.search(pstr).group('target'))
        elif(p3.search(pstr) != None):
            dic[u"revenge_date"] = ScrapeDatetime(p3.search(pstr).group('target'))
        elif(p4.search(pstr) != None):
            dic[u"date"] = ScrapeDatetime(p4.search(pstr).group('target'))
        elif(p5.search(pstr) != None):
            dic[u"teacher"] =  p5.search(pstr).group('target')
        elif(p6.search(pstr) != None):
            dic[u"time"] =  p6.search(pstr).group('target')
        elif(p7.search(pstr) != None):
            dic[u"revenge_place"] =  p7.search(pstr).group('target')
        elif(p8.search(pstr) != None):
            dic[u"remarks"] =  p8.search(pstr).group('target')
	elif(p9.search(pstr) != None):
	    dic[u"term"] =  ScrapeDatetime(p9.search(pstr).group('target'))
        #else:
            #    print "No Hit"
    return dic

def ScrapeContents(body):
    dic = {
            u"title":u"",
            u"sender":u"",
            u"info":u"",
            u"all_text":u"",
    }
    soup = BeautifulSoup(body)
    q1 = soup.findAll('span', id="form1:htmlTitle")
    q2 = soup.findAll('span', id="form1:htmlFrom")
    q3 = soup.findAll('span', id="form1:htmlMain")
    q4 = soup.findAll('span', id="form1:htmlHenko")

    #q1
    if(q1 != []):
        pstr = htmlentity2unicode(q1[0].string)
        pstr = pstr.replace(' ', '').replace(u'　', '')
        dic[u"title"] = pstr
        dic[u"all_text"] = dic[u"all_text"] + pstr
        print pstr#.encode('utf-8')
    else:
        dic[u"title"] = u''
    #q2
    if(q2 != []):
        pstr = htmlentity2unicode(q2[0].string)
        pstr = pstr.replace(' ', '').replace(u'　', '')
        dic[u"sender"] = pstr
        dic[u"all_text"] = dic[u"all_text"] + pstr
    else:
        dic[u"sender"] = u''
    #q3
    for a in q3:
        a = brRemove(a)
        dic2 = ScrapeMainHTML(a.contents)
        for key in dic2.keys():
            dic[key] = dic2[key]
        dic[u"all_text"] = dic[u"all_text"] + a.text
    #q4
    if(q4 != []):
        pstr = htmlentity2unicode(q4[0].string)
        pstr = pstr.replace(' ', '').replace(u'　', '')
        dic[u"info"] = pstr
        dic[u"all_text"] = dic[u"all_text"] + pstr
    else:
        dic[u"info"] = u''

    return dic
