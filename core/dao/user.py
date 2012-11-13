#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'
import time
from dbmanager import DbManager
from dbtables import *
class UserDao(object):
    def getSession(self):
        dbManager = DbManager.getInstance()
        if dbManager:
            return dbManager.getSession()
        else:
            return None

    def update_lastdate(self, name):
        #更新用户使用时间
        self.session = self.getSession()
        try:
            user = self.session.query(TUser).filter_by(name=name).first()
            user.last_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.commit()
        except:
            self.session.rollback()

    def register_or_login(self, name, platform, password):

        self.session = self.getSession()
        user = self.session.query(TUser).filter_by(name=name, platform=platform).first()
        try:
            if user:
                return True
            else:
                user = TUser()
                user.name=name
                user.password=password
                user.platform=platform
                user.create_date=time.strftime("%Y-%m-%d %H:%M:%S")
                user.last_date = user.create_date
                self.session.add(user)
                self.session.commit()
                return True
        except:
            self.session.rollback()