#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mar 22, 2012

@author: CLTANG
"""
import ConfigParser
import hashlib
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_
from dbtables import *
import os
import logging
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
NQ_CONFIG = ABS_PATH + \
 "../../config/xylx.conf"

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
                DbManager.__mysqlDb = create_engine(url,pool_size=20, max_overflow=-1, pool_recycle=7200) #,echo=True
                DbManager.__meta = MetaData()
                DbManager.__meta.reflect(bind=DbManager.__mysqlDb)
                DbManager.bindTables()
                global Session 
                #Session = sessionmaker(bind=DbManager.__mysqlDb,autoflush=True)
                Session = scoped_session(sessionmaker(bind=DbManager.__mysqlDb,autoflush=True))
            except Exception,e:
                print e,"===db connect error=== DbManager.getInstance()"
                logging.error(e)
                DbManager.__single = None
                raise e

        return DbManager.__single

    def getSession(self):
        Session.remove()
        return Session()

    def removeSession(self):
        if Session:
            Session.remove()

    @staticmethod
    def bindTables():
        '''完成数据库表和domain对象的映射'''
        #bind t_user
        user = DbManager.__meta.tables['user']
        mapper(User, user)
#        #bind device - t_device
#        tdevice = DbManager.__meta.tables['t_device']
#        mapper(TDevice, tdevice)
#        #bind RemoteControl - t_device_remotecontrol
#        tDeviceRemotecontrol = DbManager.__meta.tables['t_device_remotecontrol']
#        mapper(TDeviceRemotecontrol, tDeviceRemotecontrol)
#        #bind RemoteControl - t_temp_device_ios_remoteControl
#        tTempDeviceIosRemoteControl = DbManager.__meta.tables['t_temp_device_ios_remoteControl']
#        mapper(TTempDeviceIosRemoteControl, tTempDeviceIosRemoteControl)
#        #bind Location - t_device_location
#        tDeviceLocation = DbManager.__meta.tables['t_device_location']
#        mapper(TDeviceLocation, tDeviceLocation)
#        #bind tDeviceOperLog - t_device_oper_log
#        tDeviceOperLog = DbManager.__meta.tables['t_device_oper_log']
#        mapper(TDeviceOperLog, tDeviceOperLog)
#        #bind tDeviceUsinglog - t_device_using_log
#        tDeviceUsingLog = DbManager.__meta.tables['t_device_using_log']
#        mapper(TDeviceUsingLog, tDeviceUsingLog)
#
#        #bind tDeviceApnToken - t_device_apn_token
#        tDeviceApnToken = DbManager.__meta.tables['t_device_apn_token']
#        mapper(TDeviceApnToken, tDeviceApnToken)
#
#        #bind IOS tPolicy - t_policy
#        tPolicy = DbManager.__meta.tables['t_policy']
#        mapper(TPolicy, tPolicy)
#        #bind TPolicyEas - t_policy_eas
#        tPolicyEas = DbManager.__meta.tables['t_policy_eas']
#        mapper(TPolicyEas, tPolicyEas)
#        #bind TPolicyEmail - t_policy_email
#        tPolicyEmail = DbManager.__meta.tables['t_policy_email']
#        mapper(TPolicyEmail, tPolicyEmail)
#        #bind TPolicyGroup - t_policy_group
#        tPolicyGroup = DbManager.__meta.tables['t_policy_group']
#        mapper(TPolicyGroup, tPolicyGroup)
#        #bind TPolicyMdm - t_policy_mdm
#        tPolicyMdm = DbManager.__meta.tables['t_policy_mdm']
#        mapper(TPolicyMdm, tPolicyMdm)
#        #bind TPolicyPassword - t_policy_password
#        tPolicyPassword = DbManager.__meta.tables['t_policy_password']
#        mapper(TPolicyPassword, tPolicyPassword)
#        #bind TPolicyRestrictions - t_policy_restrictions
#        tPolicyRestrictions = DbManager.__meta.tables['t_policy_restrictions']
#        mapper(TPolicyRestrictions, tPolicyRestrictions)
#        #bind TPolicyScep - t_policy_scep
#        tPolicyScep = DbManager.__meta.tables['t_policy_scep']
#        mapper(TPolicyScep, tPolicyScep)
#        #bind TPolicyUser - t_policy_user
#        tPolicyUser = DbManager.__meta.tables['t_policy_user']
#        mapper(TPolicyUser, tPolicyUser)
#        #bind TPolicyVpn - t_policy_vpn
#        tPolicyVpn = DbManager.__meta.tables['t_policy_vpn']
#        mapper(TPolicyVpn, tPolicyVpn)
#        #bind TPolicyWifi - t_policy_wifi
#        tPolicyWifi = DbManager.__meta.tables['t_policy_wifi']
#        mapper(TPolicyWifi, tPolicyWifi)
#        #bind TPolicyApn - t_policy_apn
#        tPolicyApn = DbManager.__meta.tables['t_policy_apn']
#        mapper(TPolicyApn, tPolicyApn)
#        tPolicyEncrytion = DbManager.__meta.tables['t_policy_encrytion']
#        mapper(TPolicyEncrytion, tPolicyEncrytion)
#        #bind TPolicyCredential - t_policy_credential
#        tpolicyCredential = DbManager.__meta.tables['t_policy_credential']
#        mapper(TPolicyCredential, tpolicyCredential)
#        #bind TPolicyCredential - t_policy_credential
#        tpolicyCardDav = DbManager.__meta.tables['t_policy_carddav']
#        mapper(TPolicyCardDav, tpolicyCardDav)
#        #bind TPolicyCredential - t_policy_credential
#        tpolicyCalSub = DbManager.__meta.tables['t_policy_calsub']
#        mapper(TPolicyCalSub, tpolicyCalSub)
#        #bind TPolicyCredential - t_policy_credential
#        tpolicyWebClip = DbManager.__meta.tables['t_policy_webclip']
#        mapper(TPolicyWebClip, tpolicyWebClip)
#        #bind TPolicyCalDav - t_policy_caldav
#        tpolicyCalDav = DbManager.__meta.tables['t_policy_caldav']
#        mapper(TPolicyCalDav, tpolicyCalDav)
#        #bind TPolicyLDAP - t_policy_ldap
#        tpolicyLdap = DbManager.__meta.tables['t_policy_ldap']
#        mapper(TPolicyLDAP, tpolicyLdap)
#        #bind TAppBlacklisted - t_app_blacklisted
#        tAppBlacklisted = DbManager.__meta.tables['t_app_blacklisted']
#        mapper(TAppBlacklisted, tAppBlacklisted)
#
#        #bind TAppStoreBlacklisted - t_app_store_blacklisted
#        tAppStoreBlacklisted = DbManager.__meta.tables['t_app_store_blacklisted']
#        mapper(TAppStoreBlacklisted, tAppStoreBlacklisted, properties=\
#                {"app_blacklisted_fk": relationship(TAppBlacklisted)})
#
#        #bind TAppStoreDevice - t_app_store_device
#        tAppStoreDevice = DbManager.__meta.tables['t_app_store_device']
#        mapper(TAppStoreDevice, tAppStoreDevice, properties=\
#                {"app_fk": relationship(TAppStore),
#                 "device_fk": relationship(TDevice)})
#
#        #bind TAppStoreCategory - t_app_store_category
#        tAppStoreCategory = DbManager.__meta.tables['t_app_store_category']
#        mapper(TAppStoreCategory, tAppStoreCategory, properties=\
#                {"app_fk":relationship(TAppStore),
#                 "category_fk":relationship(TAppCategory)})
#
#        #bind TAppCategory - t_app_category
#        tAppCategory = DbManager.__meta.tables['t_app_category']
#        mapper(TAppCategory, tAppCategory)
#
#        #bind TAppStore - t_app_store
#        tAppStore = DbManager.__meta.tables['t_app_store']
#        mapper(TAppStore, tAppStore, properties=\
#                {"app_device_fk":relationship(TAppStoreDevice),
#                 "app_categore_fk":relationship(TAppStoreCategory)})
#
#        tGroup = DbManager.__meta.tables["t_group"]
#        mapper(TGroup, tGroup)
#
#        tDGVersion = DbManager.__meta.tables["t_document_group_version"]
#        mapper(TDGVersion, tDGVersion)
#
#        tDUVerion = DbManager.__meta.tables["t_document_user_version"]
#        mapper(TDUVerion, tDUVerion)
#
#        tTagGroup = DbManager.__meta.tables["t_document_tag_group"]
#        mapper(TTagGroup, tTagGroup)
#
#        tTagUser = DbManager.__meta.tables["t_document_tag_user"]
#        mapper(TTagUser, tTagUser)
#
#        tDocument = DbManager.__meta.tables["t_document"]
#        mapper(TDocument, tDocument)
#
#        tDocumentTag = DbManager.__meta.tables["t_document_tag"]
#        mapper(TDocumentTag, tDocumentTag)
#
#        tDocumentTagLink = DbManager.__meta.tables["t_document_tag_link"]
#        mapper(TDocumentTagLink, tDocumentTagLink, properties = \
#            {
#                "document":relationship(TDocument),
#                "d_tag":relationship(TDocumentTag)
#            })
#        tDeviceApp = DbManager.__meta.tables['t_device_app']
#        mapper(TDeviceApp, tDeviceApp)
#
#        tDeviceProfile = DbManager.__meta.tables['t_device_profile']
#        mapper(TDeviceProfile, tDeviceProfile)
#
#        t_device_securityinfo = DbManager.__meta.tables['t_device_securityinfo']
#        mapper(TDeviceSecurityinfo,t_device_securityinfo)
#
#        t_appstore_user = DbManager.__meta.tables['t_app_store_user']
#        mapper(TAppStoreUser,t_appstore_user)
#
#        t_appstore_user_group = DbManager.__meta.tables['t_app_store_user_group']
#        mapper(TAppStoreUserGroup, t_appstore_user_group)
        
        





