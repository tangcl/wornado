#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
import os

from tornado.web import RequestHandler
from core.handler.baseHandler import BaseHandler
from core.dao.video import *
from core.dao.topic import *
class VideoHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def initialize(self):
        '''
        继承RequestHandler方法,可以传入参数database,形如：
        def initialize(self, databases):
            pass
        app = Application([
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
            ])
        '''

    def get(self, user_id):
        '''
        继承get方法，传入参数
        '''
        #查询我的关注人的所有视频和视频列表
        video = VideoDao()
        return self.render("video.html", vides=video)

class UploadBeforeHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def initialize(self):
        '''
        继承RequestHandler方法,可以传入参数database,形如：
        def initialize(self, databases):
            pass
        app = Application([
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
            ])
        '''

    def get(self,topic_id):
        '''
        继承get方法，传入参数
        '''
        topicdao = TopicDao()
        try:
            text = topicdao.get_text(topic_id)
        except:
            return self.render("error.html")
        return self.render("upload.html", data={"keyword_id": topic_id, "text": text})

class UploadHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def initialize(self):
        '''
        继承RequestHandler方法,可以传入参数database,形如：
        def initialize(self, databases):
            pass
        app = Application([
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
            ])
        '''
    def post(self):
        print dir(self.request)
        try:
            request_files = self.request.files.get("file")
            if request_files:
                file = request_files[0]
                file_name = file.get("filename")
                file_body = file.get("body")
                #写入文件
                native_path = time.strftime("%Y-%m-%d %H:%M:%S")
                local_path = self.settings.get("store_path") + native_path + "/" + file_name
                with open(local_path, "wb") as f:
                    f.write(file_body)
                #检测文件是否存在
                if os.path.isfile(local_path):
                    #数据插入
                    videodao = VideoDao()
                    #视频截图模块调用。
        except:
            return self.render("error.html")