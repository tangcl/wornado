#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
import logging
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
        logging.error("DEBUG")
        return self.render("base.html",
            args1="cc",args2="dd")


    def post(self):
        super.post()

#    def redirect(self, url, permanent=False, status=None):
#        '''
#        跳转
#        '''
#        super.redirect(url, permanent=False, status)

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''

        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    '''
    用户登陆
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
            #执行正常程序
        return self.render("register.html")


    def post(self):
        pass
    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''

        return self.get_secure_cookie("user")

class RegisterHandler(BaseHandler):
    '''
    用户注册
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
        #执行正常程序
        return self.render("register.html")


    def post(self):
        print self.request.arguments

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''

        return self.get_secure_cookie("user")