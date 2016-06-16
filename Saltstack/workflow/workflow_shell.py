#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'miles.peng'
from common.cmdrun import *
class Workflow_shell():


    def create_pkg(self,projectname,sectionName,sectionVersion):
        #判断section的个数，其为list
        delimiter = ','
        _sectionName=delimiter.join(sectionName)
        _sectionVersion=delimiter.join(sectionVersion)
        cmd="/srv/salt/deploy_workflow/common/getPkgs.pl %s %s %s " %(projectname,_sectionName,_sectionVersion)
        _cmd=CmdRun()
        _cmd.run_cmd(cmd)
        return True