# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        htmlentity2unicode
# Purpose:
#
# Author:      nullpoo
#
# Created:     08/09/2012
#-------------------------------------------------------------------------------

import htmlentitydefs
import re,unicodedata

# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
	# 正規表現のコンパイル
	reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
	num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
	num10_regex = re.compile(u'#\d+', re.IGNORECASE)

	result = u''
	i = 0
	while True:
		# 実体参照 or 文字参照を見つける
		match = reference_regex.search(text, i)
		if match is None:
			result += text[i:]
			break

		result += text[i:match.start()]
		i = match.end()
		name = match.group(1)

		# 実体参照
		if name in htmlentitydefs.name2codepoint.keys():
			result += unichr(htmlentitydefs.name2codepoint[name])
		# 文字参照
		elif num16_regex.match(name):
			# 16進数
			result += unichr(int(u'0'+name[1:], 16))
		elif num10_regex.match(name):
			# 10進数
			result += unichr(int(name[1:]))

	return result