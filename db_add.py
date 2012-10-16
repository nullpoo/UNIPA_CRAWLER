# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        db_add
# Purpose:
#
# Author:      nullpoo
#
# Created:     08/09/2012
#-------------------------------------------------------------------------------

import MySQLdb
import hashlib

def add_dic(dic):
	con = MySQLdb.connect(host='[HOST_NAME]', db='[DB_NAME]', user='[USER_NAME]', passwd='[PASSWORD]', charset='utf8')
	#con.cursorclass = MySQLdb.cursors.DictCursor
	c = con.cursor()
	key = hashlib.sha256((dic["title"]+dic["sender"]+dic["date"]+dic["course"]+dic["teacher"]+dic["time"]+dic["info"]+dic["canceled_date"]+dic["revenge_date"]+dic["revenge_place"]+dic["remarks"]).encode('utf-8')).hexdigest()
	print key
	c.execute(u"insert ignore into jugyo(`key`,`title`,`sender`,`date`,`course`,`teacher`,`time`,`info`,`canceled_date`,`revenge_date`,`revenge_place`,`remarks`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (key, dic["title"],dic["sender"],dic["date"],dic["course"],dic["teacher"],dic["time"],dic["info"],dic["canceled_date"],dic["revenge_date"],dic["revenge_place"],dic["remarks"]))

	con.commit()
	con.close()
