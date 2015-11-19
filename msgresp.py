# -*- coding: utf-8 -*-

import time
from flask import make_response
import xml.etree.ElementTree as ET
from utils import WcUtils
WcUtils().coding()


class MsgResponse:
	def __init__(self):
		# Base on message type call the method
		self.TYPE_METHODS = {
			'text': self.recieve_text,
			'image': self.recieve_image,
			'voice': self.recieve_voice,
			'video': self.recieve_video,
			'shortvideo': self.recieve_shortvideo,
			'location': self.recieve_location,
			'link': self.recieve_link,
			'event': self.recieve_event,
			'unknow': self.recieve_unknow,
		}

	def response_msg(self, stream):
		xml = ET.fromstring(stream)
		msg_type = xml.find('MsgType').text
		return self.TYPE_METHODS[msg_type](xml)

	def recieve_text(self, xml):
		content = '消息类型: 文本. 您刚才对我说: "' + xml.find('Content').text + '".'
		return self.transmit_msg(xml, content)

	def recieve_image(self, xml):
		content = '消息类型: 图片. 图片地址为: "' + xml.find('PicUrl').text + '".'
		return self.transmit_msg(xml, content)

	def recieve_voice(self, xml):
		content = '消息类型: 语音. 音频格式为: "' + xml.find('Format').text + '".'
		return self.transmit_msg(xml, content)

	def recieve_video(self, xml):
		content = '消息类型: 视频. MediaId为: "' + xml.find('MediaId').text + '".'
		return self.transmit_msg(xml, content)

	def recieve_shortvideo(self, xml):
		content = '消息类型: 短视频. MediaId为: "' + xml.find('MediaId').text + '".'
		return self.transmit_msg(xml, content)

	def recieve_location(self, xml):
		content = '消息类型: 位置. 经度: ' + \
				xml.find('Location_Y').text + ',  纬度: ' + xml.find('Location_X').text + ' .'
		return self.transmit_msg(xml, content)

	def recieve_link(self, xml):
		content = '消息类型: 链接. 标题: ' + \
				xml.find('Title').text + ',  描述: ' + xml.find('Description').text + ' .'
		return self.transmit_msg(xml, content)

	def recieve_event(self, xml):
		if 'subscribe' == xml.find('Event').text:
			content = '谢谢您关注我们. 祝您天天开心!'
		else:
			content = '我暂时还没有想好怎么处理这种事情.'
		return self.transmit_msg(xml, content)

	def recieve_unknow(self, xml):
		content = '你说的到底是什么, 完全不明白哦.'
		return self.transmit_msg(xml, content)

	def transmit_msg(self, xml, content):
		tpl = '''
			<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[text]]></MsgType>
				<Content><![CDATA[%s]]></Content>
			</xml>
			'''
		from_username = xml.find('FromUserName').text
		to_username = xml.find('ToUserName').text
		resp = make_response(tpl % (from_username, to_username, str(int(time.time())), content))
		resp.content_type = 'application/xml'
		return resp


