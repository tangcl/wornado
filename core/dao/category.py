#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'
import time
from dbmanager import DbManager
from dbtables import *
class CategoryDao(object):
    def getSession(self):
        dbManager = DbManager.getInstance()
        if dbManager:
            return dbManager.getSession()
        else:
            return None



    def add_category(self, text):
        #查询我的关注用户和关注用户的视频
        self.session = self.getSession()
        try:
            category = CCategory()
            category.text = text
            category.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.add(category)
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True

    def list_category(self):
        #查询出所有的分类列表
        self.session = self.getSession()
        try:
            category = self.session.query(CCategory).all()
        except Exception, e:
            print e
            self.session.rollback()
            return False
        return category