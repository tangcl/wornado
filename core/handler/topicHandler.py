#! -*- encoding:utf-8 -*-
from core.dao.category import CategoryDao

__author__ = 'C.L.TANG'

from tornado.web import RequestHandler
from core.handler.baseHandler import BaseHandler
from core.dao.video import *
from core.dao.topic import *
class TopicListHandler(BaseHandler):
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

    def get(self, category_id):
        '''
        继承get方法，传入参数
        '''
        #获取分类下所有的题目
        topicdao = TopicDao()
        try:
            data = topicdao.list_topic(category_id)
        except:
            return self.render("error.html")
        return self.render("list_topic.html", data = {"category_id":category_id, "data": data})

class TopicCreateHandler(BaseHandler):
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

    def post(self, category_id):
        try:
            topic = self.get_argument("create")
        except:
            self.render("error.html")
        #获取category_id
        topicdao = TopicDao()
        try:
            sign = topicdao.add_topic(topic, category_id)
        except:
            sign = False
        return self.render("topic_middle.html", data = {"category_id":category_id, "data": sign})

class TopicSearchHandler(BaseHandler):
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

    def post(self, category_id):
        try:
            text = self.get_argument("search")
        except:
            self.render("error.html")
            #获取category_id
        topicdao = TopicDao()
        try:
            sign = topicdao.search_topic(text, category_id)
        except:
            sign = False
        return self.render("list_topic.html", data = {"category_id":category_id, "data": sign})
