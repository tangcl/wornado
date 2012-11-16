#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'
import time
from dbmanager import DbManager
from dbtables import *
from sqlalchemy import desc
from core.func import URL
from sqlalchemy import or_
class UserDao(object):
    def getSession(self):
        self.dbManager = DbManager.getInstance()
        if self.dbManager:
            return self.dbManager.getSession()
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

    def __del__(self):
        self.dbManager.removeSession()

    def register_or_login(self, name, platform, password):

        self.session = self.getSession()
        user = self.session.query(TUser).filter_by(name=name, password=password, platform=platform).first()
        try:
            if user:
                return True, user
            else:
                user = TUser()
                user.name=name
                user.password=password
                user.platform=platform
                user.create_date=time.strftime("%Y-%m-%d %H:%M:%S")
                user.last_date = user.create_date
                self.session.add(user)
                self.session.commit()
                return True, user
        except Exception, e:
            print e
            self.session.rollback()
            return False, None

    def del_follower(self, user_id, follower_id):
        #创建关注人
        self.session = self.getSession()
        try:
            self.session.query(FFollower).filter_by(user_id=user_id, follower_id=follower_id).delete()
            self.session.commit()
            #User表中数据-1
            #用户follower更新
            user = self.session.query(TUser).filter_by(user_id=user_id).first()
            follower = int(user.followers) -1
            if follower>0:
                user.followers = follower
                self.session.commit()
            follower = self.session.query(TUser).filter_by(user_id=follower_id).first()
            fans = int(follower.fans) - 1
            if fans>0:
                follower.fans = fans
                self.session.commit()
        except:
            return False
        return True

    def create_follower(self, user_id, follower_id):
        self.session = self.getSession()
        try:
            follower = FFollower()
            follower.user_id = user_id
            follower.follower_id = follower_id
            follower.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.add(follower)
            self.session.commit()
            #用户user表更新数据,user_id=user_id的关注数+1
            user = self.session.query(TUser).filter_by(user_id=user_id).first()
            if user:
                user.followers = int(user.followers) + 1
                self.session.commit()
            else:
                userst = TUser()
                userst.user_id = user_id
                videocount = self.session.query(VVideo).filter_by(user_id=user_id).count()
                userst.video = videocount
                userst.followers = 1
                userst.fans = 0
                userst.last_date = time.strftime("%Y-%m-%d %H:%M:%S")
                self.session.add(userst)
                self.session.commit()
                #用户follower更新
            follower = self.session.query(TUser).filter_by(user_id=follower_id).first()
            if follower:
                follower.fans = int(follower.fans) + 1
                self.session.commit()
            else:
                userst = TUser()
                userst.user_id = follower_id
                videocount = self.session.query(VVideo).filter_by(user_id=follower_id).count()
                userst.video = videocount
                userst.followers = 0
                userst.fans = 1
                userst.last_date = time.strftime("%Y-%m-%d %H:%M:%S")
                self.session.add(userst)
                self.session.commit()
        except:
            return False
        return True


    def ListFollower(self, user_id):
        self.session = self.getSession()
        followers = self.session.query(FFollower).filter_by(user_id=user_id).all()
        #查询出关注的用户的情况
        all_data = []
        for follower in followers:
            #根据用户ID，查询出用户的最新视频
            try:
                user_id = follower.follower_user.id
                video = self.session.query(VVideo).filter_by(user_id=user_id).order_by(desc(VVideo.create_date)).first()
                video.native_path = URL.make_video_url(video.native_path)
                video.native_img_path = URL.make_img_url(video.native_img_path)
                #获取当前视频数
                video_count = self.session.query(VVideo).filter_by(user_id=user_id).count()
                video.count = video_count
            except Exception, e:
                print e
                continue
            all_data.append({user_id:video})
        return all_data

    def hosUser(self):
        self.session = self.getSession()
        datas = self.session.query(TUser).order_by(desc(TUser.fans), desc(TUser.video)).all()[:10]
        print "datas:", datas
        all_data = []
        for data in datas:
            try:
                user_id = data.id
                video = self.session.query(VVideo).filter_by(user_id=user_id).order_by(desc(VVideo.create_date)).first()
                video.native_path = URL.make_video_url(video.native_path)
                video.native_img_path = URL.make_img_url(video.native_img_path)
                #获取当前视频数
                video_count = self.session.query(VVideo).filter_by(user_id=user_id).count()
                video.count = video_count
            except Exception, e:
                #点击获取热门用户后查询出他们的最新视频
                print e
                continue
            all_data.append({user_id:video})
        return all_data

    def find_user(self, user_id):
            self.session = self.getSession()
            try:
                user = self.session.query(TUser).filter_by(id=user_id).first()
                if user:
                    return True
                else:
                    return False
            except:
                return False

    def get_user(self, user_id):
        self.session = self.getSession()
        user = self.session.query(TUser).filter_by(id=user_id).first()
        return user

    def search(self, text):
        self.session = self.getSession()
        try:
            result = self.session.query(TUser).filter(or_(TUser.name.like("%"+text+"%"), TUser.sign.like("%"+text+"%"))).all()
            return result
        except:
            return False