#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Content-type: text/html\n"

import cgi
import MySQLdb
import json
import datetime

params = cgi.FieldStorage()
flag = False
if (params.has_key('fdate') and params.has_key('tdate')):
	fdate = params['fdate'].value
	tdate = params['tdate'].value
	flag = True

connect = MySQLdb.connect(host='[HOST_NAME]',db='[DB_NAME]', user='[USER_NAME]', passwd='[PASSWORD]', charset='utf8')
connect.cursorclass = MySQLdb.cursors.DictCursor
cursor = connect.cursor()

if flag == True:
	cursor.execute(u"select * from jugyo where (`date` >= '"+fdate+"' and `date` <= '"+tdate+"'"") or (`canceled_date` >= '"+fdate+"' and `canceled_date` <= '"+tdate+"'"") or (`revenge_date` >= '"+fdate+"' and `revenge_date` <= '"+tdate+"'"")")
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
