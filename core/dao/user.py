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

    def handler(self, name):
        #更新用户使用时间
        self.session = self.getSession()
        try:
            user = self.session.query(TUser).filter_by(name=name).first()
            user.last_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.commit()
        except:
            self.session.rollback()
