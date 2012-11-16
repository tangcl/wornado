#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
import os

from tornado.web import RequestHandler
from core.handler.baseHandler import BaseHandler
from core.dao.video import *
from core.dao.topic import *
from core.func.file_handler import *
from core.func.screenshot import *
class VideoHandler(BaseHandler):

    def get(self, user_id):
        '''
        继承get方法，传入参数
        '''
        #查询我的关注人的所有视频和视频列表
        videodao = VideoDao()
        video = videodao.list_video(int(user_id))
        return self.render("list_video.html", videos=video)

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
            return self.render("error.html",message="服务器错误")
        return self.render("upload.html", data={"topic_id": topic_id, "text": text})

class UploadHandler(BaseHandler):
        '''
        arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
        files - 所有通过 multipart/form-data POST 请求上传的文件
        path - 请求的路径（ ? 之前的所有内容）
        headers - 请求的开头信息
        '''
        def post(self):
            topic_id = self.get_argument("topic_id")
            user_id = self.current_user
            try:
                request_files = self.request.files.get("file")
                if request_files:
                    file = request_files[0]
                    file_name = file.get("filename")
                    file_body = file.get("body")
                    #写入文件
                    native_path = sha1_encode(file_body) + r"." + file_name.split(".")[1]
                    local_path = self.settings.get("store_path") + native_path
                    file_object = open(local_path, 'wb')
                    file_object.writelines(file_body)
                    file_object.close( )
                    native_img_path = sha1_encode(file_body) +".jpg"
                    local_img_path = self.settings.get("img_path") + native_img_path
                    shandler = ScreenHandler()
                    sign = shandler.handler(local_path, local_img_path)
                    if sign:
                        videodao = VideoDao()
                        create_sign = videodao.create_video(local_path, native_path, topic_id=topic_id,user_id=user_id, native_img_path=native_img_path, local_img_path = local_img_path)
                        if create_sign:
                            return self.render("video_success_middle.html")
                        else:
                            #删除本地图片，本地视频
                            os.remove(local_path)
                            os.remove(local_img_path)
                            return self.render("error.html",message="服务器错误")
                    else:
                        os.remove(local_path)
                        return self.render("error.html",message="服务器错误")
                else:
                    return self.render("error.html",message="服务器错误")
            except:
                return self.render("error.html",message="服务器错误")

class NewestHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def get(self):
        #获取全网最新100个视频
        videodao = VideoDao()
        videos = videodao.newest_video()
        if videos:
            return self.render("list_video.html", videos = videos)
        else:
            return self.render("error.html",message="服务器错误")

class CommentHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def post(self, video_id):
        #获取全网最新100个视频
        comment_text = self.get_argument("comment")
        user_id = int(self.current_user)
        videodao = VideoDao()
        sign = videodao.add_comment(comment_text=comment_text,user_id=user_id, video_id=video_id)
        if sign:
            return self.redirect("/newest")
        else:
            return self.render("error.html",message="服务器错误")

class DetailHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def get(self, video_id):
        videodao = VideoDao()
        data = videodao.get_video_byId(video_id)
        if data:
            return self.render("detail_video.html", data = data)
        else:
            return self.render("error.html",message="服务器错误")


class PraiseHandler(BaseHandler):
    '''
    arguments - 所有的 GET 或 POST 的参数,字典类型，self.request.arguments.get(name, [])
    files - 所有通过 multipart/form-data POST 请求上传的文件
    path - 请求的路径（ ? 之前的所有内容）
    headers - 请求的开头信息
    '''
    def get(self, video_id):
        videodao = VideoDao()
        user_id = int(self.current_user)
        sign = videodao.add_praise(user_id, int(video_id))
        if sign:
            return self.redirect("/newest")
        else:
            return self.render("error.html",message="您只能赞一次")
