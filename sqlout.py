#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Content-Type: text/plain;charset=utf-8\n"

import cgi
import MySQLdb
import json
import datetime

params = cgi.FieldStorage()
flag = True
if (params.has_key('fdate') and params.has_key('tdate')):
	fdate = params['fdate'].value
	tdate = params['tdate'].value
	flag = True

connect = MySQLdb.connect(host='HOST_NAME',db='DB_NAME', user='USER_NAME', passwd='USER_PASSWORD', charset='utf8')
connect.cursorclass = MySQLdb.cursors.DictCursor
cursor = connect.cursor()

fdate = '2012-04-08'
tdate = '2013-04-08'

if flag == True:
	cursor.execute(u"""
    select * from jugyo where (`date` >= %s and `date` <= %s)
    or (`canceled_date` >= %s and `canceled_date` <= %s)
    or (`revenge_date` >= %s and `revenge_date` <= %s)""", (fdate, tdate, fdate, tdate, fdate, tdate))
else:
	cursor.execute(u"select * from jugyo")

rows = cursor.fetchall()

count = 0
for dic in rows:
	for key,value in dic.items():
		if type(value) == datetime.date:
			 rows[count][key] =  value.strftime('%Y-%m-%d')
	count+=1
print json.dumps(rows, indent=2, ensure_ascii=False).encode('utf-8')
