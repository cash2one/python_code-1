#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'miles.peng'
import sys
import pdb
from optparse import OptionParser
from  configparser import Getconfig
from deploy_workflow import Root_dir
class Optionparse():
#'''init and set argvs from command line '''
    def opt_parser_command(self):
        usage = "usage: %prog [options] arg"
        parser = OptionParser(usage)
        parser.add_option("-p", "--project name", dest="projectName",
                          help="Project name like goc")
        parser.add_option("-m", "--section name",
                          help="section name like gameserver", dest="sectionName")
        parser.add_option("-v", "--section version",
                          help="section version like v2.5.15", dest="sectionVersion")
        parser.add_option("-d", "--Database version",
                          help="Database  version like 3", dest="databaseVersion")
        parser.add_option("-s", "--Is db stop",action="store_true",
                          help="Database need stop in maintain", dest="is_db_stop")

        (options, args) = parser.parse_args()
        _option={}
        # projectName,sectionName,sectionVersion must input
        if options.projectName and options.sectionName and options.sectionVersion:
            _option['sectionName']=options.sectionName.split(',')
            _option['projectName']=options.projectName
            _option['databaseVersion']=options.databaseVersion.split
            _option['need_stop']=options.is_db_stop
            if len(options.sectionName.split(',')) != len(str(options.sectionVersion).split(',')):
                if len(options.sectionName.split(',')) > 1 and  len(str(options.sectionVersion).split(','))==1:
                    for _length in range(len(options.sectionName.split(','))) :
                        _option['sectionVersion'][_length]=str(options.sectionVersion).split(',')[0]
                else:
                    print "[ERROR] model name is not match version"
                    sys.exit(1)
            else:
                _option['sectionVersion']=options.sectionVersion.split(',')
        else:
            parser.error("incorrecter of arguments must input -p -m -v")

        self.check_optin(_option)
        return  _option

    #'''解析基于界面输入的参数'''
    def opt_parser_interface(self):
        _length=len(sys.argv)
        _option={}
        if _length>=4:
            try:
                _option["projectName"]=sys.argv[1]
                _option["sectionName"]=sys.argv[2].split(',')
                _option["sectionVersion"]=str(sys.argv[3]).split(',')
            except BaseException,e:
                print("[ERROR] Input argv error,some values is null,%s") %str(e)
                sys.exit(1)
            if _length>=5:
                _option["databaseVersion"]=sys.argv[4]
                if _length==6:
                    _option['need_stop']=sys.argv[5]
        else:
            print("[ERROR] incorrecter of arguments in projectName,sectionName,sectionVersion")
            sys.exit(1)

        if len(_option["sectionName"]) == len(_option["sectionVersion"]) :
            pass
        elif len(_option["sectionName"]) >1 and  len(_option["sectionVersion"]) ==1 :
            _option["sectionVersion"]=[]
            for _length in range(len(_option["sectionName"])):
                _option["sectionVersion"][_length]=str(sys.argv[2]).split(',')[0]
        else:
            print("[ERROR] param sectionName length is not the same as sectionVersion ")
            sys.exit(1)

        self.check_optin(_option)
        return _option

    #检查输入sectionName是否在配置文件中存在
    def check_optin(self,_option):

        projectName=_option["projectName"]
        sectionNames=_option["sectionName"]
        configName=Root_dir+'/ini/'+str(projectName).strip()+'_workflow.ini'
        sectionList=[]
        for sectionName in sectionNames:
            #sectionName=sectionName[2:-2]
            _getconfig=Getconfig()
            _param=_getconfig.getconfig(sectionName,configName)
            if _param:
                sectionList.append(sectionName)

        #当sectionName=all时，其为唯一值
        if "all" in sectionList and len(sectionList) != 1:
            print "[ERROR] section =All is only section"
            sys.exit(1)

        return  True




