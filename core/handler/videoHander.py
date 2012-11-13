#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'

from tornado.web import RequestHandler
from core.handler.baseHandler import BaseHandler
class MainHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def initialize(self):
        '''
        继承RequestHandler方法,可以传入参数database,形如：
        def initialize(self, databases):
            pass
        app = Application([
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
            ])
        '''

    def get(self):
        '''
        继承get方法，传入参数
        '''
        return self.render("base.html",
            args1="cc",args2="dd")


    def post(self):
        super.post()
