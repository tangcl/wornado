#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'
import time
from dbmanager import DbManager
from dbtables import *
class TopicDao(object):
    def getSession(self):
        dbManager = DbManager.getInstance()
        if dbManager:
            return dbManager.getSession()
        else:
            return None

    def get_text(self, topic_id):
        self.session = self.getSession()
        try:
            topic = self.session.query(TTopic).filter(TTopic.id==topic_id).first()
        except:
            return False
        return topic

    def add_topic(self, text, category_id):
        self.session = self.getSession()
        try:
            topic = TTopic()
            topic.text = text
            topic.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            topic.last_date = topic.create_date
            self.session.add(topic)
            self.session.commit()
            #然后add关系
            category_topic = CCategoryTopic()
            category_topic.category_id = category_id
            category_topic.topic_id = topic.id
            category_topic.create_date = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.add(category_topic)
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return True

    def list_topic(self, category_id):
        self.session = self.getSession()
        try:
            topic = self.session.query(TTopic).filter(TTopic.id==CCategoryTopic.topic_id, CCategoryTopic.category_id==category_id).all()
        except:
            self.session.rollback()
            return False
        return topic

    def search_topic(self, keyword, category_id):
        self.session = self.getSession()
        try:
            result = self.session.query(TTopic).filter(TTopic.text.like("%"+keyword+"%"), CCategoryTopic.topic_id==TTopic.id, CCategoryTopic.category_id==category_id).all()
            self.session.commit()
        except:
            self.session.rollback()
            return False
        return result