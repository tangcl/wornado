#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
import logging
from core.handler.baseHandler import BaseHandler
from core.dao.user import UserDao
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
        return self.render("list_video.html",
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
        print "login"
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
        if self.current_user:
            return self.render("success.html", user_id = int(self.get_secure_cookie("user")))
        else:
            return self.render("register.html")

    def post(self):
        name = self.get_argument("user")
        platform = self.get_argument("platform")
        password = self.get_argument("password")
        userdao = UserDao()
        try:
            sign, user = userdao.register_or_login(name=name, platform=platform, password=password)
        except:
            return self.render("error.html", message="服务器错误")
        if sign:
            self.set_secure_cookie("user", str(user.id))
            self.render("success.html", user_id=user.id)
        else:
            #注册或者登录失败，返回登录页
            self.render("register.html")

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class CreateFollowerHandler(BaseHandler):

    def get(self, follower_id):
        '''
        创建关注关系
        '''
        user_id = self.get_secure_cookie("user")
        userdao = UserDao()
        try:
            sign = userdao.create_follower(user_id, follower_id)
        except:
            return self.render("error.html", message="服务器错误")
        self.set_secure_cookie("user", user_id)
        self.redirect("/list_follower")

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class DelFollowerHandler(BaseHandler):
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

    def get(self, follower_id):
        '''
        创建关注关系
        '''
        user_id = self.get_secure_cookie("user")
        userdao = UserDao()
        try:
            sign = userdao.del_follower(user_id, follower_id)
        except:
            return self.render("error.html", message="服务器错误")
        self.set_secure_cookie("user", user_id)
        self.redirect("/list_follower")

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class ListFollowerHandler(BaseHandler):
    '''
    列出用户的关注情况
    '''
    def get(self):
        user_id = self.get_secure_cookie("user")
        userdao = UserDao()
        try:
            data = userdao.ListFollower(int(user_id))
        except:
            return self.render("error.html", message="服务器错误")
        if self.settings.get("debug"):
            return self.render("list_follower.html",datas=data)
        else:
            #返回json数据
            pass

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class HotUserHandler(BaseHandler):
    '''
    列出用户的关注情况
    '''
    def get(self):
        #查询出fans数最多的用户100个用户
        hot_user = UserDao()
        try:
            datas = hot_user.hosUser()
        except:
            return self.render("error.html", message="服务器错误")
        return self.render("list_follower.html", datas = datas)

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class ShowUserHandler(BaseHandler):
    '''
    列出用户的关注情况
    '''
    def get(self,user_id):
        #查询出fans数最多的用户100个用户
        user_detail = UserDao()
        try:
            datas = user_detail.get_user(user_id)
        except:
            return self.render("error.html", message="服务器错误")
        return self.render("user_detail.html", datas = datas)

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")

class SearchUserHandler(BaseHandler):
    '''
    列出用户的关注情况
    '''
    def post(self):
        #查询出fans数最多的用户100个用户
        text = self.get_argument("text")
        userdao = UserDao()
        try:
            result = userdao.search(text)
            return self.render("list_user.html", result = result)
        except:
            self.render("error.html", message="没有该用户")

    def get_current_user(self):
        '''
        查询cookie中的值，进行用户认证
       '''
        return self.get_secure_cookie("user")