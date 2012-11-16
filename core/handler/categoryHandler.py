#! -*- encoding:utf-8 -*-
from core.dao.category import CategoryDao

__author__ = 'C.L.TANG'

from tornado.web import RequestHandler
from core.handler.baseHandler import BaseHandler
from core.dao.video import *
class CategoryListHandler(BaseHandler):

    def get(self):
        '''
        继承get方法，传入参数
        '''
        #创建一个分类
        list_category = CategoryDao()
        try:
            data = list_category.list_category()
        except:
            return self.render("error.html", message="服务器错误")
        if data:
            return self.render("list_category.html", list_category=data)
        else:
            return self.redirect("/admin")