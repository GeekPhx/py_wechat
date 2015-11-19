# -*- coding: utf-8 -*-

TOKEN = 'update_token'


# 中文乱码解决方案
def coding(coding = 'utf-8'):
	import sys
	reload(sys)
	sys.setdefaultencoding(coding)


