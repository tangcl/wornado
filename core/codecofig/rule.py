#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
'''
本文件为所有URL路由文件
'''
from tornado import web
from core.handler.userHander import *
application = [
    (r"/static/(.*)", web.StaticFileHandler, {"path": "../../static"}),
    (r"/", BaseHandler),
    (r"/login", IndexHandler),
]