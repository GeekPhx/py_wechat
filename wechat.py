# -*- coding: utf-8 -*-

from flask import Flask, request, make_response
from msgresp import MsgResponse
from utils import WcUtils
WcUtils().coding()

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def wechat_entry():
	if request.method == 'GET':
		data = request.args
		if WcUtils().auth(data):
			return make_response(data.get('echostr'))
	else:
		stream = request.stream.read()
		return MsgResponse().response_msg(stream)

if __name__ == '__main__':
	app.run()

