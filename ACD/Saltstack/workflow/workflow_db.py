#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'miles.peng'
'''数据库工作流方法'''
import  os
import  sys
sys.path.append("..")
from common.manageDB import *
from common.configparser import *
from deploy_workflow import Root_dir


class Workflow_DB():
    def __init__(self):
        filename_ini=Root_dir+"/ini/common.ini"
        _getconfig=Getconfig()
        _config=_getconfig.getconfig("workflow_db",filename_ini)
        self.configNameDB=Root_dir+_config["configNameDB"]
        self.bak_dir=_config["bak_dir"]
        self.update_script=Root_dir+_config["update_script"]
        self.s3_dir=_config["s3_dir"]
        self.expiration=_config["expiration"]
        self.check_sql=_config["check_sql"]

   # '''db back操作包含back，clear old bak，sync to s3！'''
    def db_back(self,dbhost,dbuser,dbpasswd,dbname,projectname):
        _db=ManageDB()
        TargPath=_db.backupDB(dbhost,dbuser,dbpasswd,dbname,projectname,self.bak_dir)
        if _db.clearBak(TargPath,self.expiration):
            print "%s Clear old bak files success"%TargPath
        if _db.sync2S3(TargPath,projectname,self.s3_dir):
            print "%s DB back files up S3 success"%projectname
        return  True





    def db_update(self,dbhost,dbuser,dbpasswd):
        update_script=self.update_script
        _db=ManageDB()
        if _db.updateDB(dbhost,dbuser,dbpasswd,update_script):
            return  True


    def db_check(self,dbhost,dbuser,dbpasswd,checkDB,checkTable,dbVersion,check_sql):
        _db=ManageDB()
        if _db.checkDB(dbhost,dbuser,dbpasswd,checkDB,checkTable,dbVersion,check_sql):
            return  True





#'''正常状态下数据库工作流，包括DB back,clear old bak,rsync to s3，Update，check version，rm update script操作，上述操作定义在manageDB模块的ManageDB类中'''
    def normal_workflow(self,projectname,databaseVersion):
        _config=Getconfig()
        _data=_config.getconfig(projectname,self.configNameDB)
        dbhost=_data.get("dbhost",False)
        dbuser=_data.get("dbuser",False)
        dbpasswd=_data.get("dbpasswd",False)
        dbname=str(_data.get("dbname",False)).split(",")
        checkDB=_data.get("check_db",False)
        checkTable=_data.get("check_table",False)
        dbVersion=databaseVersion
        #check param not null
        if dbhost and dbuser and dbpasswd and dbname and checkDB and checkTable and dbVersion:
            self.db_back(dbhost,dbuser,dbpasswd,dbname,projectname)
            self.db_update(dbhost,dbuser,dbpasswd)
            self.db_check(dbhost,dbuser,dbpasswd,checkDB,checkTable,dbVersion,self.check_sql)
            return  True
        else:
            print("[ERROR] Some values in db config is null ,pls check it ")
            sys.exit(1)



