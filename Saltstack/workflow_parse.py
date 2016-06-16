#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'miles.peng'

from deploy_workflow import Root_dir
from workflow.workflow_shell import *
from common.configparser import *
from workflow.workflow_salt import *
from workflow.workflow_db import *


import time
import pdb
class Workflow_parse():

    def workflow_nodb_command(self,projectname,sectionName,sectionVersion):
        #按projectName,sectionName 创建PKG包

        self.create_pkg(projectname,sectionName,sectionVersion)
        #按参数推送PKG到所有的host
        self.push_pkg(projectname,sectionName)

        #对所有的HOST执行stop-release-check-start操作
        self.deploy_workflow(projectname,sectionName,sectionVersion,is_stop=False)
        return True

    def workflow_stopservice_updatedb(self,projectname,sectionName,sectionVersion,databaseVersion):
        self.create_pkg(projectname,sectionName,sectionVersion)
        self.push_pkg(projectname,sectionName)
        #停止所有服务
        self.stop_all_service(projectname)
        self.db_update(projectname,databaseVersion)
        self.deploy_workflow(projectname,sectionName,sectionVersion,is_stop=True)
        return True


    def workflow_updatedb(self,projectname,sectionName,sectionVersion,databaseVersion):
        self.create_pkg(projectname,sectionName,sectionVersion)
        self.push_pkg(projectname,sectionName)

        self.db_update(projectname,databaseVersion)
        self.deploy_workflow(projectname,sectionName,sectionVersion,is_stop=False)
        return True

#按sectionName取得Host，filename，desc_dir信息，调用salt执行分发操作
    def push_pkg(self,projectname,sectionName):
        configName=Root_dir+"/ini/"+projectname+"_workflow.ini"
        #configName="/srv/salt/deploy_workflow/ini/"+projectname+"_workflow.ini"
        print"-------------------Start Push PKG------------------------------------------"
        #print "get configname.."+configName

        #如果有“all”，则一定写在第一个
        if sectionName[0].lower()=="all":
            _config=Getconfig()
            _sectionNames=_config.getconfig("all",configName)["include"].split(',')
        else:
            _sectionNames=sectionName

        for _sectionName in _sectionNames:
                _get_section_config=Getconfig()
                _section_data=_get_section_config.getconfig(_sectionName,configName)
                for host_group in _section_data["host"].split("|"):
                    for _host in host_group.split(','):
                        self._push_pkg_via_section(_host,_section_data["module"],_section_data["filename"],projectname,_section_data["desc_dir"],_section_data["upload_sls"])

        print"-------------------End Push PKG------------------------------------------"
        return True


    def _push_pkg_via_section(self,host,moudleName,filename,projectName,desc_dir,upload_sls):
        filename_values=""
        for _count in range(len(filename.split(','))):
            _string="%s: %s "%(moudleName.split(',')[_count],filename.split(',')[_count])
            filename_values=filename_values +' , '+_string
        pillar="{'fileName': {%s}, 'project_name': %s,'desc_dir': %s}" % (filename_values[2:],projectName,desc_dir)
        _workflow=Workflow_salt()
        if _workflow._salt_run_state_argv(host,upload_sls,pillar):
            print "Upload PKG to host=%s projectName=%s filename=%s success"% (host,projectName,filename)
        return True




    def stop_all_service(self,projectname):
        print "-------------------------Start stop_all_service---------------------"
        configName=Root_dir+"/ini/"+projectname+"_workflow.ini"
        operate="stop"
        stop_list=[]
        _config=Getconfig()
        _modules=_config.getconfig("all",configName)["include"]
        for _module in _modules.split(','):
            _data=_config.getconfig(_module,configName)
            stop_sls="sls.stop_service"
            start_service=_data["start_service"]
            #service=_data["service"]
            hosts=_data["host"]
            for host_group in hosts.split('|'):
                for _host in host_group:
                    data=[_host,stop_sls,start_service]
                    stop_list.append(data)
        #删除重复的stop service 操作
        new_stop_list=self.remove_duplicate_list(stop_list)
        for (_host,stop_sls,start_service) in new_stop_list:
            _workflow=Workflow_salt()
            _workflow._salt_run_state_argv(_host,stop_sls,start_service)
        print "-------------------------End stop_all_service---------------------"
        return True



    def db_update(self,projectname,databaseVersion):
        print "--------------------------Start DB update-----------------------"
        _workflow=Workflow_DB()
        _workflow.normal_workflow(projectname,databaseVersion)
        print "--------------------------End DB update-----------------------"
        return True

    def deploy_workflow(self,projectname,sectionName,sectionVersion,is_stop):
        print "------------------------Start deploy ---------------------------------"

        configName=Root_dir+"/ini/"+projectname+"_workflow.ini"
        #print "configname is %s" %configName
        _getconfig=Getconfig()
        check_section_version=[]
        if sectionName[0].lower()=="all":
            _sections=_getconfig.getconfig("all",configName)["include"].split(',')
            for length in range(len(_sections)):
                check_section_version.append(sectionVersion[0])
        else:
            _sections=sectionName
            check_section_version=sectionVersion

        for _length in range(len(_sections)):
            _section=_sections[_length]
            _check_version=check_section_version[_length]
            _section_data=_getconfig.getconfig(_section,configName)
            _host_group=_section_data["host"].split('|')
            _module=_section_data["module"]
            _filename=_section_data["filename"]
            _desc_dir=_section_data["desc_dir"]
            deploy_sls=_section_data["deploy_sls"]
            time_wait_workflow=_section_data["timewait_workflow"].strip()
            time_wait_lb=_section_data["timewait_lb"].strip()
            check_section=_section_data["check_module"]
            start_service=_section_data["start_service"]
            stop_sls="sls.stop_service"
            start_sls="sls.start_service"
            #获取串行操作的HOST Name
            for _hosts in _host_group:
                is_wait_lb=False
                if len(_host_group)>1:
                    is_wait_lb=True
                #并行操作
                for _host in _hosts.split(','):
                    #关闭服务
                    if not is_stop:
                        #service=_section_data["service"]
                        self.stop_service(_host,stop_sls,start_service)
                    #deploy
                    filename_values=""
                    for _count in range(len(_filename.split(','))):
                         _string="%s: %s "%(_module.split(',')[_count],_filename.split(',')[_count])
                         filename_values=filename_values +' , '+_string
                    pillar="{'fileName': {%s},'project_name': %s,'desc_dir': %s}" % (filename_values[2:],projectname,_desc_dir)
                    self.deploy_service_pillar(_host,deploy_sls,pillar)
                    print "%s %s %s has deployed"%(_host,projectname,filename_values[2:])
                    self.check_section_version(_host,check_section,_check_version)
                    self.start_service(_host,start_sls,start_service)
                    print "%s %s Operating complete \n"%(_host,_section)
                if is_wait_lb:
                    print "Waiting for service start %s s curr_time=%s"%(str(time_wait_lb),time.ctime())
                    time.sleep(float(time_wait_lb))
                    print "End Waiting cur_time=%s \n"%(time.ctime())
            #print "Waiting %s s for next section cur_time=%s"%(str(time_wait_workflow),time.ctime())
            time.sleep(float(time_wait_workflow))
            #print "End waiting for next section cur_time=%s \n"%(time.ctime())

        print "------------------------End deploy ---------------------------------"





    #def remove_duplicate_list(seq, idfun=None): # Alex Martelli ******* order preserving
    def remove_duplicate_list(slef,l1):
        l2=[]
        [l2.append(i) for i in l1 if not i in l2]
        return l2
    #    if idfun is None:
    #        def idfun(x): return x
    #    seen = {}
    #    result = []
    #    for item in seq:
    #        marker = idfun(item)
    #        # in old Python versions:
    #        # if seen.has_key(marker)
    #        # but in new ones:
    #        if marker not in seen:
    #            seen[marker] = 1
    #            result.append(item)


        return result



    def start_service(self,_host,start_sls,start_service):
        pillar="{'start_service': %s}"% start_service
        _workflow=Workflow_salt()
        _workflow._salt_run_state_argv(_host,start_sls,pillar)
        print "Host=%s service %s has started" % (_host,start_service)
        return  True

    def stop_service(self,_host,stop_sls,start_service):
        pillar="{'start_service': %s}"% start_service
        _workflow=Workflow_salt()
        _workflow._salt_run_state_argv(_host,stop_sls,pillar)
        print "Host=%s service %s has stoped" % (_host,start_service)
        return  True



    def deploy_service_pillar(self,host,deploy_sls,pillar):
        _workflow=Workflow_salt()
        _workflow._salt_run_state_argv(host,deploy_sls,pillar)
        #print "Host=%s has deployed" % host
        return  True


    def check_section_version(self,host,check_section,sectionVersion):
        _workflow=Workflow_salt()
        if _workflow.remot_check_version(host,check_section,sectionVersion):
            print "Check host=%s %s = %s success"%(host,check_section,sectionVersion)
            return True




    def create_pkg(self,projectname,sectionName,sectionVersion):
        print "-----------------Create PKG starting----------------------------------"
        _workflow=Workflow_shell()
        _workflow.create_pkg(projectname,sectionName,sectionVersion)
        print "Create %s-%s PKG files versioin %s success" % (projectname,sectionName,sectionVersion)
        print "-----------------Create PKG end----------------------------------"
        return True


    def operate_service(self,host,service,operate):
        _workflow=Workflow_salt()
        _workflow._salt_service_operate(host,service,operate)
        return  True