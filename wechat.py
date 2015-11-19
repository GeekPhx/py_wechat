# -*- coding: utf-8 -*-

import time
import hashlib
import xml.etree.ElementTree as ET
from flask import Flask, request, make_response
import dicter
import setting
setting.coding()
token = setting.TOKEN

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def wechat_entry():
	if request.method == 'GET':
		data = request.args

		signature = data.get('signature', '')
		timestamp = data.get('timestamp', '')
		nonce = data.get('nonce', '')
		echostr = data.get('echostr', '')

		ary = [timestamp, nonce, token]
		ary.sort()
		arystr = ''.join(ary)

		if (hashlib.sha1(arystr).hexdigest() == signature):
			return make_response(echostr)
		else:
			pass
	else:
		stream = request.stream.read()
		xml = ET.fromstring(stream)

		from_username = xml.find('FromUserName').text
		to_username = xml.find('ToUserName').text
		msg_type = xml.find('MsgType').text
		if 'text' == msg_type:
			query = xml.find('Content').text
			msg = dicter.translate(query)
		else:
			msg = '对不起, 系统正在完善中. 目前仅支持文本消息.'

		rtn_xml = "\
			<xml>\
				<ToUserName><![CDATA[%s]]></ToUserName>\
				<FromUserName><![CDATA[%s]]></FromUserName>\
				<CreateTime>%s</CreateTime>\
				<MsgType><![CDATA[%s]]></MsgType>\
				<Content><![CDATA[%s]]></Content>\
				<FuncFlag>0</FuncFlag>\
			</xml>"

		resp = make_response(rtn_xml % (from_username, to_username, str(int(time.time())), 'text' , msg))
		resp.content_type = 'application/xml'
		return resp


if __name__ == '__main__':
	app.run()

