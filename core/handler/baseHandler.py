#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'

from tornado.web import RequestHandler
from core.dao.user import *
class BaseHandler(RequestHandler):
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
        if self.current_user is None:
            return self.redirect(self.settings.get("login_url"))
        else:
            user_id = int(self.current_user)
            userdao = UserDao()
            u = userdao.find_user(user_id)
            if u:
                return self.render("success.html", user_id=int(self.current_user))
            else:
                #删除cookie
                self.clear_all_cookies()
                return self.redirect("/")


    def post(self):
        pass

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''

        return self.get_secure_cookie("user")

