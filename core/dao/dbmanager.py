#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mar 22, 2012

@author: 章红兵
"""
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

    def __del__(self):
        self.dbManager.removeSession()

    def test_applist(self):
        #join所有表查询,查询出所有与app关联的属性的条件。
        joinall = self.session.query(TAppStore).join(TAppStoreDevice).join(TAppStoreCategory).\
        filter(and_(TDevice.os==0,TDevice.versioNum=="10A403", TDevice.id==TAppStoreDevice.deviceId, TAppStoreCategory.appCategoryId==1,TAppStore.type == 0, or_(TAppStore.name.like('%aa%'), TAppStore.pkgname.like("%pkg%")))).all()
        print joinall[0].id, joinall[0].name, joinall[0].createTime
        print "分类:", joinall[0].app_categore_fk[0].category_fk.name

    def test_applist_by_class(self):
        '''
        按大类获取
        '''
        result = self.session.query(TAppStore).filter(and_(TAppStore.platform==0, TAppStore.status==0, or_(TAppStore.osVersion<="5.3", TAppStore.osVersion == None),or_(TAppStore.name.like('%%'), TAppStore.pkgname.like("%%")))).all()
        print result

    def test_applist_by_category(self):
        '''
        按大类获取
        '''
        result = self.session.query(TAppStore).filter(and_(TAppStore.platform==0, TAppStore.status==0, TAppStoreCategory.appCategoryId == TAppCategory.id,TAppStoreCategory.appStoreId == TAppStore.id, TAppCategory.id==1,or_(TAppStore.osVersion<="5.3", TAppStore.osVersion == None),or_(TAppStore.name.like('%%'), TAppStore.pkgname.like("%%")))).all()
        print result

    def test_appdetail(self):
        #获得app的具体详情
        apps = self.session.query(TAppStore).filter(and_(TAppStore.id==2,  )).first()
        print apps.app_categore_fk[0].category_fk.name
        #获取app在该机器上的使用情况
        all_result = []
        for app in apps:
            result = self.session.query(TDeviceApp.status).filter(TDeviceApp.appId==app.id, TDeviceApp.deviceId == TDevice.id, TDevice.udid == "25b32148ddf68a792b6bf32392cca62251b5cde2").first()

            if result:
                app.install_status = result[0]
                all_result.append(result)
        else:
            pass
        print all_result

    def test_appdetail_status(self):
        #查看是否该机器上的应用本机状态
        result = self.session.query(TDeviceApp).filter(and_(TDeviceApp.deviceId==7, TDeviceApp.appId==1)).first()
        print result.status

    def test_appdetailall(self):
        result = self.session.query(TAppStore).join(TAppStoreDevice).filter(and_(TDevice.os=='ios', TDevice.udid=="37a0dd7c91781c482b32f00608c28100e5f5292b", TDeviceApp.deviceId==TDevice.id, TAppStore.type==0, TAppStore.id== TAppStoreDevice.appStoreId, TAppStore.id==1 )).first()
        device_app = self.session.query(TDeviceApp).filter(and_(TDeviceApp.deviceId==result.app_device_fk[0].device_fk.id, TDeviceApp.appId==result.id)).first()
        print device_app.status

    def test_category(self):
        result = self.session.query(TAppCategory).join(TAppStoreCategory).filter(and_(TAppStoreCategory.appStoreId == TAppStore.id, TAppStore.platform==0, TAppStore.type==0, TAppStore.status==0,TAppStoreCategory.appCategoryId == TAppCategory.id)).all()
        print result[0].name

    def test_appdetailistallfilter(self):
        result = self.session.query(TAppStore).join(TAppStoreDevice).\
        filter(and_(TDevice.id == TDeviceApp.deviceId == TAppStoreDevice.deviceId, \
            TDevice.loginId == TDeviceApp.loginId, TDevice.udid=="37a0dd7c91781c482b32f00608c28100e5f5292b", TDeviceApp.status==1,)).all()[0:2]
        print result

    def test_appdetailownerfilter1(self):
        #获取我的应用列表
        #所有历史已安装的
        #根据用户
        loginId = self.session.query(TDevice.loginId).filter(TDevice.udid=="16497cb7f32054a3160c1b457db4e183b99da206").first()
        if loginId:loginId = loginId[0]
        else:raise ValueError("error")
        result_installs = self.session.query(TAppStore).join(TAppStoreDevice).filter(and_(TDeviceApp.appId == TAppStore.id,TDeviceApp.loginId==loginId, TDeviceApp.status == 1, TAppStore.status == 0)).all()
        result_updates = self.session.query(TAppStore).join(TAppStoreDevice).filter(and_(TDeviceApp.appId == TAppStore.id,TDeviceApp.loginId==loginId, TDeviceApp.status == 2, TAppStore.status == 0)).all()
        result_deletes = self.session.query(TAppStore).join(TAppStoreDevice).filter(and_(TDeviceApp.appId == TAppStore.id,TDeviceApp.loginId==loginId, TDeviceApp.status == 3, TAppStore.status == 0)).all()
        all_result = []
        for result_install in result_installs:
            result_install.install_status = 1
            print result_install.app_categore_fk[0].category_fk.name
            all_result.append(result_install)
        for result_update in result_updates:
            result_update.install_status = 2
            print result_update.app_categore_fk
            all_result.append(result_update)
        for result_delete in result_deletes:
            result_delete.install_status = 3
            all_result.append(result_delete)
        return all_result
    def test_appdetailownerfilter2(self):
        #获取我的应用列表
        #本机已安装但有更新的
        result = self.session.query(TAppStore).filter(and_(TDeviceApp.deviceId == TDevice.id, TDeviceApp.appId == TAppStore.id, TDevice.udid=="37a0dd7c91781c482b32f00608c28100e5f5292b", TDeviceApp.status == 2, TAppStore.status == 0)).all()
        print result

    def test_appdetailownerfilter3(self):
        '''
        #获取我的应用列表
        #本机未安装但曾经安装过的
        #用户名下的所有应用减去本机的已安装应用,采用app_id的集合进行集合操作，在重新查询出这些应用
        '''
        #查询出本机下所有安装应用
        all_apps = self.session.query(TAppStore).filter(and_(TDevice.udid=='16497cb7f32054a3160c1b457db4e183b99da206', \
            TDeviceApp.deviceId == TDevice.id,TAppStore.id == TDeviceApp.appId, TDeviceApp.status !=3,TAppStore.status == 0)).all()
        print all_apps
        #查询出用户名下所有应用
        #1.查询出用户名
        loginId = self.session.query(TDevice.loginId).filter(TDevice.udid=="16497cb7f32054a3160c1b457db4e183b99da206").first()
        if loginId:loginId = loginId[0]
        else:raise ValueError("error")
        print loginId
        #2.查询出用户名下所有应用
        user_apps = self.session.query(TAppStore).filter(and_(TDeviceApp.appId == TAppStore.id,TDeviceApp.loginId==loginId)).all()
        print user_apps
        result = set(all_apps)&set(user_apps)
        print result
        return result
    def test_getMyApp(self):
        '''
        #获取我的应用列表
        #本机已安装没有更新的
        '''
        result = self.session.query(TAppStore).filter(and_(TDeviceApp.deviceId == TDevice.id, TDeviceApp.appId == TAppStore.id, TDevice.udid=="37a0dd7c91781c482b32f00608c28100e5f5292b", TDeviceApp.status == 1)).all()
        print result[0].app_categore_fk[0].category_fk.name

    def test_InstallApp(self):
        #根据appId查询出应用地址
        result = self.session.query(TAppStore.source).filter(and_(TAppStore.id == 1)).first()
        print result

    def test_andoird_installthen(self):
        #需要在app_store表中查询出应用的属性，在t_app_store_device表中创建关联关系。在插入到t_device_app表中所有数据
        device = self.session.query(TDevice).filter(and_(TDevice.udid == "16497cb7f32054a3160c1b457db4e183b99da206")).first()


        #查询中间表中是否存在该数据
        middle_app = self.session.query(TAppStoreDevice).filter(and_(TAppStoreDevice.deviceId == device.id, TAppStoreDevice.appStoreId == 1)).first()

        if middle_app:
            return False
        else:
            #加入到中间表
            print "device", device.id
            tAppStoreDevice = TAppStoreDevice()
            tAppStoreDevice.id = "fssfdsfdss"
            tAppStoreDevice.deviceId = device.id
            tAppStoreDevice.appStoreId = 1
            import time
            tAppStoreDevice.createTime = time.strftime("%Y-%m-%d %H:%M:%S")
            self.session.add(tAppStoreDevice)

            app = self.session.query(TAppStore).filter(TAppStore.id == 1).first()
            print app

            #向device_app表插入数据

            tDeviceApp = TDeviceApp()
            tDeviceApp.deviceId = device.id
            tDeviceApp.name = app.name
            tDeviceApp.packageName = app.pkgname
            tDeviceApp.version = app.version
            tDeviceApp.size = app.size
            tDeviceApp.appId = 1
            tDeviceApp.loginId = device.loginId
            tDeviceApp.status = 1
            self.session.add(tDeviceApp)
            self.session.commit()
            return True

    def test_UnstallApp(self):
    #根据appId查询出应用地址
        #先查询出deviceId

        try:
            results = self.session.query(TDeviceApp).filter(TDevice.udid == "37a0dd7c91781c482b32f00608c28100e5f5292b", TDevice.id == TDeviceApp.deviceId).first()
            results.status = 3
            self.session.commit()
        except:
            self.session.rollback()

    def test_installAll(self):
        results = self.session.query(TAppStore).filter(TDevice.udid == "16497cb7f32054a3160c1b457db4e183b99da206", \
            TDevice.id == TDeviceApp.deviceId==TAppStoreDevice.deviceId, TAppStore.id == TAppStoreDevice.appStoreId, TDeviceApp.status == 2).all()
        print results

    def test_check_version(self):
        #通过设备ID,查询出用户ID
        user_id = self.session.query(TDevice.loginId).filter(TDevice.udid == "16497cb7f32054a3160c1b457db4e183b99da202").first()[0]

        #查询出用户版本号，组版本号
        #1.查询出组id
        group_id = self.session.query(TUser.groupId).filter(TUser.loginId == user_id).first()[0]

        #2. 查询出版本号
        group_version = self.session.query(TDGVersion.version).filter(TDGVersion.groupId == group_id).first()[0]
        #3. 查询出用户版本号
        user_version = self.session.query(TDUVerion.version).filter(TDUVerion.loginId == user_id).first()[0]
        print group_version
        print user_version
        #2个版本号相加sha1
        version = hashlib.sha1(str(group_version+user_version)).hexdigest()
        print version
        return version

    def test_find_file(self):
        #查询出当前用户所含有的所有的标签ID，所有标签ID查询出所有的文档ID，文档中间表数据
        #1 查询出用户登陆ID
        user_id = self.session.query(TDevice.loginId).filter(TDevice.udid == "16497cb7f32054a3160c1b457db4e183b99da206").first()[0]
        #根据用户ID查询出所有标签ID，和用户所对应的组的tagID集合
        #1.查询出组id
        group_id = self.session.query(TUser.groupId).filter(TUser.loginId == user_id).first()[0]
        #查询出组tag
        group_tag = self.session.query(TTagGroup.tagId).filter(TTagGroup.groupId == group_id).all()
        #查询出用户tag
        print "group_tag:", group_tag
        user_tag = self.session.query(TTagUser.tagId).filter(TTagUser.loginId == user_id).all()
        print "user_tag:", user_tag
        group_tag.extend(user_tag)
        print "all_tag:", group_tag
        all_tag = [tag[0] for tag in group_tag if group_tag]
        print "LIST all_tag:", all_tag
        #根据所有标签，查询出所有的doc文档
        result = self.session.query(TDocumentTagLink).filter(TDocumentTagLink.tagId.in_(all_tag)).all()

        print dir(result)
        print dir(result[0].document)

    def test_handler_category(self):
        results = self.session.query(TDocumentTagLink).filter(TDocumentTagLink.docId == 1).all()[0]

        print results.d_tag.name

    def test_getUserLogin(self):
        #目前阶段用户登录只是用username,password,clientUID做登录判断。
        result = self.session.query(TUser).join(TDevice).filter(TUser.loginId == TDevice.loginId =="tangchaolin", TUser.password == "E10ADC3949BA59ABBE56E057F20F883E", TDevice.udid == "16497cb7f32054a3160c1b457db4e183b99da207").all()
        print dir(result)
        print type(result)
        print result[0]
        print type(result[0])
        print dir(result[0])

    def test_handler_device_app(self):
        result = self.session.query(TDeviceApp).filter(and_(TDeviceApp.deviceId==7, TDeviceApp.appId==1)).first()
        return result

    def test_add_All_app(self):
        #增加一个应用
        tDeviceApp = TDeviceApp()
        tDeviceApp.deviceId = "dsfasdferwvfdsawdfs"
        tDeviceApp.name = "腾讯QQ"
        tDeviceApp.packageName = "com.tx.qq"
        tDeviceApp.version = "5.3"
        tDeviceApp.size = 33
        tDeviceApp.status = 1
        self.session.add(tDeviceApp)
        self.session.commit()
if __name__=="__main__":
    #测试根据id查询软件信息
    class_test = Check_Sql()
    class_test.test_add_All_app()




