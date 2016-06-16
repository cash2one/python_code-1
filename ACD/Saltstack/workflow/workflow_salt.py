#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'miles.peng'
import sys
sys.path.append("..")
from common.configparser import *
from common.cmdrun import *
from deploy_workflow import Root_dir

'''工作流基本类型类，包含基于salt实现的服务的开启与关闭，文件分发，文件部署等'''
class Workflow_salt():
    check_salt_script="coc_deploy.get_files_info"
    def __init__(self):
        filename_ini=Root_dir+"/ini/common.ini"
        _getconfig=Getconfig()
        _config=_getconfig.getconfig("Workflow_salt",filename_ini)
        self.check_salt_script=_config["check_salt_script"]
    #'''用于单个服务的操作'''

    def _salt_service_operate(self,host,service,operate):
        salt_cmd="sudo salt '%s' service.%s %s" % (host,operate,service)
        salt_mode = "module"
        _cmd=CmdRun()
        if _cmd.run_salt(salt_cmd,salt_mode):
            return  True






    def _salt_run_state_argv(self,host,argv,pillar):
        salt_cmd="sudo salt '%s' state.sls %s pillar='%s'" % (host,argv,pillar)
        salt_mode = "state"
        _cmd=CmdRun()
        if _cmd.run_salt(salt_cmd,salt_mode):
            return  True

    def _salt_run_state_noargv(self,host,argv):
        salt_cmd="sudo salt '%s' state.sls %s" % (host,argv)
        salt_mode = "state"
        _cmd=CmdRun()
        if _cmd.run_salt(salt_cmd,salt_mode):
            return  True


   # '''通过salt section方法获得远程Host上section的版本号,与输入版本号比对，返回True/False'''
    def remot_check_version(self,host,check_section,sectionVersion):

        _values=self._salt_checkVersion(host,self.check_salt_script,check_section)
        if sectionVersion.strip() != _values.strip():
            print "[ERROR] check files version error host = %s ,check_section=%s sectionVersion=%s output =%s" % (host,check_section,sectionVersion.strip(),_values.strip())
            sys.exit(1)
        else:
            return  True



    def _salt_checkVersion(self,host,checkScript,argv):
        salt_cmd="sudo salt '%s' %s '%s'" %(host,checkScript,argv)
        _cmd=CmdRun()
        out=_cmd.run_salt_out(salt_cmd)
        return  str(out)
