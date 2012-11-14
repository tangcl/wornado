#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'
import time
from dbmanager import DbManager
from dbtables import *
class VideoDao(object):
    def getSession(self):
        dbManager = DbManager.getInstance()
        if dbManager:
            return dbManager.getSession()
        else:
            return None



    def list_video(self, user_id):
        #查询我的关注用户和关注用户的视频
        self.session = self.getSession()
        video = self.session.query(VVideo).filter_by(user_id=user_id).all()
        return video