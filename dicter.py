# -*- coding: utf-8 -*-

import json
import urllib
import setting
setting.coding()

status = {
	'0': '正常',
	'20': '要翻译的文本过长',
	'30': '无法进行有效的翻译',
	'40': '不支持的语言类型',
	'50': '无效的key',
	'60': '无词典结果'
}


# 此处需要的信息可以到有道词典API官网申请
# 申请没有什么限制条件, 所以这里我保留了这些信息
#
# http://fanyi.youdao.com/openapi.do
# ?keyfrom=Dicter&key=2046816003&
# type=data&doctype=json&version=1.1&q=query
def translate(query):
	params = urllib.urlencode({
		'keyfrom': 'Dicter',
		'key': '2046816003',
		'type': 'data',
		'doctype': 'json',
		'version': '1.1',
		'q': query
	})
	response = urllib.urlopen('http://fanyi.youdao.com/openapi.do?%s' % params)
	reslt = json.loads(response.read())
	msg = ''
	errorCode = reslt['errorCode']
	if errorCode == 0:
		for ts in reslt['translation']:
			msg += '有道翻译: \n' + ts
		try:
			basic = reslt['basic']
			msg += '\n词语发音: \n[ ' + basic['phonetic'] + ' ]'
			if basic['explains']:
				msg += '\n基本解释: \n' + ' | '.join(basic['explains'])
		except KeyError, e:
			pass
		try:
			web = reslt['web']
			msg += '\n网络释义: '
			for item in web:
				msg += '\n' + item['key'] + ': ' + ' | '.join(item['value'])
		except KeyError, e:
			pass
	else:
		msg = status[str(errorCode)]
	return msg

