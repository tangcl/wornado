#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mar 22, 2012

@author:
"""
import time
import ConfigParser
import hashlib
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_
import os
import logging
from core.dao.dbtables import *
from sqlalchemy import desc

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
NQ_CONFIG = ABS_PATH + \
 "/../../config/xylx.conf"
Session = None
class DbManager:
    '''
    管理mysqlalchemy 数据库连接 表映射 和 session 
    '''
    __single = None
    __meta = None
    __mysqlDb = None
    
    def __init__(self):
        if DbManager.__single:
            raise DbManager.__single
        DbManager.__single = self
        
    @staticmethod
    def getInstance():
        '''获取单例 绑定数据源和映射表'''
        if DbManager.__single is None:
            DbManager.__single = DbManager()
            cf = ConfigParser.ConfigParser()
            cf.read(NQ_CONFIG)
            url = "%s://%s:%s@%s/%s?charset=%s" \
                % (cf.get("db", "db_engine"), cf.get("db", "db_user"), \
                cf.get("db", "db_pass"), cf.get("db", "db_host"),  \
                cf.get("db", "db_name"), cf.get("db", "db_charset")
                       )
            ''' 正式环境 不需要设字符集
            url = "%s://%s:%s@%s/%s" \
                % (cf.get("db", "db_engine"), cf.get("db", "db_user"), \
                cf.get("db", "db_pass"), cf.get("db", "db_host"),  \
                cf.get("db", "db_name"))
            '''
            try:
                DbManager.__mysqlDb = create_engine(url,pool_size=20, max_overflow=-1, pool_recycle=7200,echo=True) #
                DbManager.__meta = MetaData()
                DbManager.__meta.reflect(bind=DbManager.__mysqlDb)
                DbManager.bindTables()
                global Session

                #Session = sessionmaker(bind=DbManager.__mysqlDb,autoflush=True)
                Session = scoped_session(sessionmaker(bind=DbManager.__mysqlDb,autoflush=True))
                print Session
            except Exception,e:
                print e,"===db connect error=== DbManager.getInstance()"
                logging.error(e)
                DbManager.__single = None
                raise e

        return DbManager.__single
    
    @staticmethod
    def bindTables():
        '''完成数据库表和domain对象的映射'''
        #bind t_user
        tuser = DbManager.__meta.tables['user']
        mapper(TUser, tuser)

        video = DbManager.__meta.tables['video']
        mapper(VVideo, video)

        follower = DbManager.__meta.tables['follower']
        mapper(FFollower, follower, properties=\
            {"follower_user": relationship(TUser)})

        category = DbManager.__meta.tables['category']
        mapper(CCategory, category)

        category_topic = DbManager.__meta.tables['category_topic']
        mapper(CCategoryTopic, category_topic)

        topic = DbManager.__meta.tables['topic']
        mapper(TTopic, topic,properties=\
            {"category_topic": relationship(CCategoryTopic)})


        
    def getSession(self): 
        Session.remove()
        return Session()
    
    def removeSession(self):      
        if Session:
            Session.remove()

class Check_Sql():

    def __init__(self):
        self.dbManager = DbManager.getInstance()
        #如果连接失败 获取实例时会再尝试连接一次
    #    dbManager = DbManager.getInstance()
        if self.dbManager:
            self.session = self.dbManager.getSession()
        else:
            raise

    def create_follower(self):
        #关注一个用户
        id=1
        id2=2
        follower = FFollower()
        follower.user_id = id
        follower.follower_id = id2
        follower.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
        self.session.add(follower)
        self.session.commit()

    def find_follower(self):
        #查询出关注用户
        user_id = 1
        followers = self.session.query(FFollower).filter_by(user_id=user_id).all()
        #查询出关注的用户的情况
        for follower in followers:
            #根据用户ID，查询出用户的视频
            try:
                user_id = follower.follower_user.id
                video = self.session.query(VVideo).filter_by(user_id=user_id).order_by(desc(VVideo.create_date)).first()
                print video.videopath
                video_count = self.session.query(VVideo).filter_by(user_id=user_id).count()
                print "video_count:",video_count
            except:
                continue

    def del_follower(self):
        user_id = 1
        follower_id = 2
        user = self.session.query(FFollower).filter_by(user_id=user_id, follower_id=follower_id).delete()
        self.session.commit()

    def find_topic(self):
        category_id = 1
        topic = self.session.query(TTopic).filter(TTopic.id==CCategoryTopic.topic_id, CCategoryTopic.category_id==category_id).all()
        print "topic:", topic

if __name__=="__main__":
    #测试根据id查询软件信息
    class_test = Check_Sql()
    class_test.find_topic()




