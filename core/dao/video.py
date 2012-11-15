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

    def create_video(self, local_path, native_path, topic_id, user_id, native_img_path="", local_img_path=""):
        self.session = self.getSession()
        try:
            video = VVideo()
            video.user_id = user_id
            video.native_path = native_path
            video.local_path = local_path
            video.native_img_path = native_img_path
            video.local_img_path = local_img_path
            video.topic_id = topic_id
            video.comment = 0
            video.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            video.last_date = video.create_date
            self.session.add(video)
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True
    def list_video(self, user_id):
        #查询我的关注用户和关注用户的视频
        self.session = self.getSession()
        video = self.session.query(VVideo).filter_by(user_id=user_id).all()
        return video