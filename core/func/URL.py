#! -*- encoding:utf-8 -*-
__author__ = 'CLTANG'

#构造URL下发给客户端
import sys
from core.codecofig import setting
def get_ip():
    if sys.platform.startswith("linux"):
        import socket
        import fcntl
        import struct
        def get_ip_address(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])
        ip = get_ip_address('eth0')
    else:
        import socket
        myname = socket.getfqdn(socket.gethostname(  ))
        ip = socket.gethostbyname(myname)
    return ip
def make_video_url(file_name):
    #获取本机IP
    ip = get_ip()
    url = "http://"+ip+":"+ str(setting.port) + "/downloadstore/"+file_name
    print url
    return url

def make_img_url(file_name):
    ip = get_ip()
    url = "http://"+ip+":"+ str(setting.port) + "/downloadimg/"+file_name
    print url
    return url