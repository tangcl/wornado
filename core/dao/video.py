#! -*- encoding:utf-8 -*-
from sqlalchemy.sql.expression import desc

__author__ = 'CLTANG'
import time
import random
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

            #用户视频数+1
            user = self.session.query(TUser).filter_by(id=user_id).first()
            user.video = user.video+1
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True
    def list_video(self, user_id):
        #查询我的关注用户和关注用户的视频
        self.session = self.getSession()
        data = {}
        try:
            videos = self.session.query(VVideo).filter(VVideo.user_id==user_id).order_by(desc(VVideo.create_date)).all()[:100]
            #从该视频相关类别中选择5个答案，同真实答案混合在一起。
            user = self.session.query(TUser).filter(TUser.id==user_id).first()
            for video in videos:
                #查询xylxcore表，获取到这个用户是否回答过这个视频的答案
                xylxcore = self.session.query(XylxCore).filter(XylxCore.video_id==video.id, XylxCore.user_id==user_id, XylxCore.status==1).first()
                if xylxcore is None:
                    wrong = []
                    topic_id = video.topic_id
                    #查询category_topic表.
                    topic = self.session.query(TTopic).filter(CCategoryTopic.topic_id==topic_id, TTopic.id==topic_id).first()
                    #在该类别中选择5个题目
                    category = self.session.query(CCategoryTopic).filter(CCategoryTopic.topic_id == topic_id).first()
                    all = self.session.query(TTopic).filter(TTopic.id==CCategoryTopic.topic_id, CCategoryTopic.topic_id!=topic_id, CCategoryTopic.category_id == category.category_id).all()[:5]
                    wrong.extend(all)
                    wrong.insert(random.randrange(0,5),topic)
                    video.wrong = wrong
                else:
                    video.wrong = None
            data["user"] = user
            data["videos"] = videos
        except Exception, e:
            print "error:", e
            return False

        return data

    def newest_video(self, user_id):
        self.session = self.getSession()
        data = {}
        try:

            videos = self.session.query(VVideo).order_by(desc(VVideo.create_date)).all()[:100]
            #从该视频相关类别中选择5个答案，同真实答案混合在一起。
            user = self.session.query(TUser).filter(TUser.id == user_id).first()
            for video in videos:
                #查询xylxcore表，获取到这个用户是否回答过这个视频的答案
                xylxcore = self.session.query(XylxCore).filter(XylxCore.video_id==video.id, XylxCore.user_id==user_id, XylxCore.status==1).first()
                if xylxcore is None:
                    wrong = []
                    topic_id = video.topic_id
                    #查询category_topic表.
                    topic = self.session.query(TTopic).filter(CCategoryTopic.topic_id==topic_id, TTopic.id==topic_id).first()
                    #在该类别中选择5个题目
                    category = self.session.query(CCategoryTopic).filter(CCategoryTopic.topic_id == topic_id).first()
                    all = self.session.query(TTopic).filter(TTopic.id==CCategoryTopic.topic_id, CCategoryTopic.topic_id!=topic_id, CCategoryTopic.category_id == category.category_id).all()[:5]
                    wrong.extend(all)
                    wrong.insert(random.randrange(0,5),topic)
                    video.wrong = wrong
                else:
                    video.wrong = None
            data["user"] = user
            data["videos"] = videos

        except Exception, e:
            print "error:", e
            return False
        return data

    def add_comment(self, comment_text, user_id, comment_id=None,  video_id=None):

        self.session = self.getSession()

        try:
            video_comment = Comment()
            video_comment.user_id = user_id
            video_comment.text = comment_text
            video_comment.video_id = video_id
            video_comment.comment_id = comment_id
            video_comment.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.add(video_comment)
            self.session.commit()

            #视频表comment+1
            comment = self.session.query(VVideo).filter_by(id=video_id).first()
            comment.comment+=1
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True

    def get_video_byId(self, video_id):
        #根据一个视频ID，获取这个视频下的所有的评论，评论的评论，生成结构树
        self.session = self.getSession()
        try:
            video = self.session.query(VVideo).filter_by(id=video_id).first()
            #根据视频ID，查询出所有的评论
            comments = self.session.query(Comment).filter_by(video_id=video_id).all()

#            for comment in comments:
#                user = self.session.query(TUser).filter_by(id=user_id).first()
#                comment.user = user
            return video, comments
        except:
            self.session.rollback()
            print "eerror"
            return False

    def add_praise(self, user_id, video_id):
        #插入到表Index_praise中，唯一索引
        self.session = self.getSession()
        try:
            index_praise = self.session.query(IndexPraise).filter(IndexPraise.user_id==user_id, IndexPraise.video_id==video_id).first()
            if index_praise:
                #已经存在数据了，不让在+1
                return False
            else:
                index_praise = IndexPraise()
                index_praise.user_id = user_id
                index_praise.video_id = video_id
                index_praise.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
                self.session.add(index_praise)
                self.session.commit()
                #视频表中praise+1
                video = self.session.query(VVideo).filter_by(id=video_id).first()
                video.praise+=1
                self.session.commit()
                return True
        except Exception, e:
            print "error",e
            self.session.rollback()
            return False

    def check_answer(self, video_id, topic_id, user_id):
        #插入到表Index_praise中，唯一索引
        self.session = self.getSession()
        try:
            video = self.session.query(VVideo).filter(VVideo.id==video_id, VVideo.topic_id==topic_id).first()
            if video:
                #根据视频ID，和提交的题目ID,获取得到数据，表示答对
                xylxcore = self.session.query(XylxCore).filter(XylxCore.video_id==video_id, XylxCore.user_id==user_id, XylxCore.status==1).first()
                if xylxcore:
                    return True
                xylxcore = XylxCore()
                xylxcore.video_id = video_id
                xylxcore.user_id = user_id
                xylxcore.count = 1
                xylxcore.status = 1
                xylxcore.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
                xylxcore.last_date = time.strftime("%Y-%m-%d %H:%M:%S")
                self.session.add(xylxcore)
                self.session.commit()
                return True
            else:
                #没有回答正确
                return False
        except Exception, e:
            print "error",e
            self.session.rollback()
            return False

    def list_video_by_topic(self, topic_id, user_id):
        self.session = self.getSession()
        data = {}
        try:

            videos = self.session.query(VVideo).filter(VVideo.topic_id==topic_id).order_by(desc(VVideo.create_date)).all()
            #从该视频相关类别中选择5个答案，同真实答案混合在一起。
            user = self.session.query(TUser).filter(TUser.id == user_id).first()
            for video in videos:
                #查询xylxcore表，获取到这个用户是否回答过这个视频的答案
                xylxcore = self.session.query(XylxCore).filter(XylxCore.video_id==video.id, XylxCore.user_id==user_id, XylxCore.status==1).first()
                if xylxcore is None:
                    wrong = []
                    topic_id = video.topic_id
                    #查询category_topic表.
                    topic = self.session.query(TTopic).filter(CCategoryTopic.topic_id==topic_id, TTopic.id==topic_id).first()
                    #在该类别中选择5个题目
                    category = self.session.query(CCategoryTopic).filter(CCategoryTopic.topic_id == topic_id).first()
                    all = self.session.query(TTopic).filter(TTopic.id==CCategoryTopic.topic_id, CCategoryTopic.topic_id!=topic_id, CCategoryTopic.category_id == category.category_id).all()[:5]
                    wrong.extend(all)
                    wrong.insert(random.randrange(0,5),topic)
                    video.wrong = wrong
                else:
                    video.wrong = None
            data["user"] = user
            data["videos"] = videos

        except Exception, e:
            print "error:", e
            return False
        return data
