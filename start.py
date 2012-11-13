#! -*- encoding:utf-8 -*-
__author__ = 'C.L.TANG'
'''
启动脚本
'''
import os
import logging.config
import tornado
from tornado import web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

class Server(object):
    def start_single(self,port, app):
        '''
        单一进程
        '''
        server = HTTPServer(app)
        server.listen(port)
        IOLoop.instance().start()

    def start_sub_multi(self,port, app):
        '''
        一个进程中多个子进程
        '''
        server = HTTPServer(app)
        server.bind(port)
        server.start(0)  # Forks multiple sub-processes
        IOLoop.instance().start()

    def start_multi(self,port):
        '''
        多个子进程,根据CPU个数创建
        '''
        sockets = tornado.netutil.bind_sockets(port)
        tornado.process.fork_processes(0)
        server = HTTPServer()
        server.add_sockets(sockets)
        IOLoop.instance().start()

if __name__ == "__main__":
    from core.codecofig.setting import settings
    from core.codecofig import rule
    app = rule.application
    web_app = web.Application(app, **settings)
    server = Server()
    #Linux环境才可以使用
#    server.start_sub_multi(8888, app)
    server.start_single(8888, web_app)





