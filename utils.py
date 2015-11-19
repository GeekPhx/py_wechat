# -*- coding: utf-8 -*-

import hashlib


class WcUtils:
	def __init__(self):
		self.coding()

	def coding(self, coding = 'utf-8'):
		import sys
		reload(sys)
		sys.setdefaultencoding(coding)

	# Auth, checkout the signature
	def auth(self, data):
		timestamp = data.get('timestamp', '')
		nonce = data.get('nonce', '')
		token = 'update_token'

		ary = [timestamp, nonce, token]
		ary.sort()
		ast = ''.join(ary)

		signature = data.get('signature', '')
		if hashlib.sha1(ast).hexdigest() == signature:
			return True
		else:
			return False
