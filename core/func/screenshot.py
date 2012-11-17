#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'

import os
class ScreenHandler(object):

    def handler(self, local_path, img_local_path):
        #判断时候存在该文件
        print "local_path:", local_path
        with open(local_path, "rb") as f:
            data = f.read()

        print "in screenhot:", len(data)
        #文件存在，则判断文件后缀
        if local_path.endswith("MOV"):
            #ios文件
            order = "ffmpeg -i %s -y -f mjpeg -vframes 1 -an %s" % (local_path, img_local_path)
        elif local_path.endswith("mp4"):
            order = "ffmpeg -itsoffset -2 -i %s -f  rawvideo -vcodec mjpeg -vframes 1 -an %s" % (local_path, img_local_path)
        else:
            return False

        #处理文件
        sign = self._handler(order)
        return sign

    def _handler(self, order):
        try:
            os.system(order)
            return True
        except:
            return False