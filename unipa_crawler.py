# -*- coding: utf-8 -*-
#サーバアクセス用のライブラリ
from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib
#エンコードなどの文字列処理用
import re, unicodedata
#XML処理用
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
#数値参照を文字参照に
#from htmlentity2unicode import htmlentity2encode
#スクレイピング処理
from ScrapeContents import brRemove, ScrapeMainHTML, ScrapeContents
#日付整形用
from ScrapeDatetime import ScrapeDatetime
#DB追加用
from db_add import add_dic

#GETリクエストを実行
def GetRequest(uri):
	req = urllib2.Request(uri)
	req.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0')
	opener = urllib2.build_opener()
	opener.add_handler(urllib2.HTTPCookieProcessor(cj))
	#リクエスト送信
	res = opener.open(req)
	#レスポンス取得
	result = res.read()

	return result

#POSTリクエストを実行
def PostRequest(uri,params):
	#パラメータをURLエンコード
	params = urllib.urlencode(params)
	#リクエスト作成
	req = urllib2.Request(uri)
	opener = urllib2.build_opener()
	opener.add_handler(urllib2.HTTPCookieProcessor(cj))
	#ヘッダ追加
	req.add_header('Content-Type','application/x-www-form-urlencoded')
	req.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0')
	#パラメータ追加
	req.add_data(params)
	#リクエスト送信
	res = opener.open(req)
	#レスポンス取得
	result = res.read()

	return result

#ページに埋めこまれているセッションを取得
def GetSessionID(srchtml):
	soup = BeautifulSoup(srchtml)
	q = soup.findAll('input',id="com.sun.faces.VIEW")
	session_id = q[0]['value']

	return session_id

#----------------------main-----------------------
cj = cookielib.CookieJar()
#root = Element('root')

#ログインページの取得
url = "http://portal.sa.dendai.ac.jp/up/faces/login/Com00505A.jsp"
body = GetRequest(url)
SessionID = GetSessionID(body)
print SessionID

#認証処理をしてトップページを取得
url = "https://portal.sa.dendai.ac.jp/up/faces/login/Com00505A.jsp"
#POSTパラメータ作成
params = {
	'form1:htmlUserId':'[ID]',
		'form1:htmlPassword':'[PASSWORD]',
		'com.sun.faces.VIEW':SessionID,
		'form1:login.x':'0',
		'form1:login.y':'0',
		'form1':'form1'}
body = PostRequest(url,params)
SessionID = GetSessionID(body)
print SessionID

#トップページの[全授業]ボタンを押す
url = "https://portal.sa.dendai.ac.jp/up/faces/up/po/Poa00601A.jsp"
#POSTパラメータ作成
params = {
	'form1:Poa00201A:htmlParentTable:2:htmlHeaderTbl:0:allJugyo.x':'',
	'com.sun.faces.VIEW':SessionID,
	'form1':'form1'}
body = PostRequest(url,params)
SessionID = GetSessionID(body)
print SessionID

#トップページの[全て表示]を押す
url = "https://portal.sa.dendai.ac.jp/up/faces/up/po/Poa00601A.jsp"
#POSTパラメータ作成
params = {
	'form1:Poa00201A:htmlParentTable:2:htmlDisplayOfAll:0:allInfoLinkCommand':'',
	'com.sun.faces.VIEW':SessionID,
	'form1':'form1'}
body = PostRequest(url,params)
SessionID = GetSessionID(body)
print SessionID

#項目数取得
soup = BeautifulSoup(body)
q = soup.findAll('span', id="form1:Poa00201A:htmlParentTable:htmlDetailTbl2:htmlListCount")
info_count = int(q[0].contents[0].replace('&#20214;',""))
print info_count

#詳細ページ取得
for i in range(info_count):
	url="https://portal.sa.dendai.ac.jp/up/faces/up/po/pPoa0202A.jsp?fieldId=form1:Poa00201A:htmlParentTable:0:htmlDetailTbl2:"+str(i)+":linkEx2"
	body2 = GetRequest(url)
	body = unicodedata.normalize('NFKC', body2.decode('utf-8'))

	dic = ScrapeContents(body)
	#for item,item2 in dic.items():
	#	print item,item2
	add_dic(dic)
	removeurl = "https://portal.sa.dendai.ac.jp/up/faces/ajax/up/co/RemoveSessionAjax?target=null&windowName=Poa00201A&pcClass=com.jast.gakuen.up.po.PPoa0202A"
	GetRequest(removeurl)
#result =  htmlentity2unicode(tostring(root)).encode('utf-8')
#print result
#out_f = open('xml_test.xml','w')
#out_f.write(result)
#out_f.close()
