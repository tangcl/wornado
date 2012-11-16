#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
'''
本文件为所有URL路由文件
'''
from core.handler.userHander import *
from core.handler.videoHander import *
from core.handler.adminHandler import *
from core.handler.categoryHandler import *
from core.handler.topicHandler import *
from tornado.web import ErrorHandler
from tornado import web
application = [
#    (r"/static/(.*)", web.StaticFileHandler, {"path": "../../static"}),
    (r"/register/", RegisterHandler),
    (r"/logout", LogoutHandler),
    (r"/", BaseHandler),
    (r"/error",ErrorHandler),
    (r"/list_follower", ListFollowerHandler),
    (r"/downloadstore/(.*)", web.StaticFileHandler, {"path": "./video/store"}),
    (r"/downloadimg/(.*)", web.StaticFileHandler, {"path": "./video/img"}),
    (r"/hot_user", HotUserHandler),
    (r"/create_follower/(.*?)", CreateFollowerHandler),
    (r"/del_follower/(.*?)", DelFollowerHandler),
    (r"/list_video/(.*?)", VideoHandler),
    (r"/upload_before/(.*?)", UploadBeforeHandler),
    (r"/upload", UploadHandler),
    (r"/admin", AdminCreateCategoryHandler),
    (r"/list_category", CategoryListHandler),
    (r"/create_topic/(.*?)", TopicCreateHandler),
    (r"/list_topic/(.*?)", TopicListHandler),
    (r"/search_topic/(.*?)", TopicSearchHandler),
    (r"/newest", NewestHandler),
    (r"/video_comment/(.*?)", CommentHandler),
    (r"/video_detail/(.*?)", DetailHandler),
    (r"/add_praise/(.*?)", PraiseHandler),
    (r"/show_user/(.*?)", ShowUserHandler),
    (r"/search_user", SearchUserHandler),
]