#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
__author__ = 'miles.peng'
Root_dir="/srv/salt/deploy_workflow"
import sys
sys.path.append(Root_dir)
#print sys.path
from common.optparser import *
from workflow_parse import *
import pdb


'''分析启动参数--参数确认--生成pkg--数据库操作--salt相关工作流操作'''
def run_workflow(_option):


    projectname=_option["projectName"]
    sectionName=_option["sectionName"]
    sectionVersion=_option["sectionVersion"]


    #无数据库相关操作
    if not _option.get("databaseVersion",False):
        _workflow=Workflow_parse()
        _workflow.workflow_nodb_command(projectname,sectionName,sectionVersion)
        print "ALL deploy success"

    #需要停止服务在更新DB
    elif _option.get("need_stop",False):
        databaseVersion=_option["databaseVersion"]
        _workflow=Workflow_parse()
        _workflow.workflow_stopservice_updatedb(projectname,sectionName,sectionVersion,databaseVersion)
        print "ALL deploy success"
    #有数据库更新操作，但无需先停止服务应用的操作
    else:
        databaseVersion=_option["databaseVersion"]
        _workflow=Workflow_parse()
        _workflow.workflow_updatedb(projectname,sectionName,sectionVersion,databaseVersion)
        print "ALL deploy success"


if __name__=="__main__":
    _opt=Optionparse()
    _option=_opt.opt_parser_interface()
#    pdb.set_trace()
    run_workflow(_option)
