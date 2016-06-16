#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


from modifyConfig import  *
from common import  *


def get_build(config_name_pkg,section,version):
    if section == "all":
        section_get_collect=get_conf(config_name_pkg,"common").get("include",None)
        if section_get_collect:
            section_collect=section_get_collect.split(",")
        else:
            msg="include no found!"
            logMsg("getpkg",msg,2)
            sys.exit(1)
    else:
        section_collect=section.split(",")

    #clear build dir
    default_param=get_conf(config_name_pkg,"common")
    buildHomePath=default_param.get("buildhomepath",None)
    buildName=default_param.get("buildname",None)
    modi_config_file=default_param.get("releaseconf",None)
    build_path=buildHomePath+'/'
    _cmd_clear="cd %s && rm -r %s && mkdir -p %s"%(build_path,buildName,buildName)
    logMsg("getpkg",_cmd_clear,1)
    run_cmd(_cmd_clear)

    package_path=build_path+buildName
    for section_loop in section_collect:
        _param=get_conf(config_name_pkg,section_loop)
        srcGameSrv=_param.get("srcgamesrv",None)
        rsyncTagPath=_param.get("rsynctagpath",None)
        uploadPkgs=_param.get("uploadpkgs",None)
        #as "rsync -vzrtopg --delete --progress qa@54.223.79.251::DeploymentHome/apache-tomcat/webapps/rollit_html/ ./rollit_html"
        _cmd_rsync="cd %s && rsync -vzrtopg --delete --progress qa@%s::%s/%s/ ./%s"%(package_path,srcGameSrv,rsyncTagPath,uploadPkgs,uploadPkgs)
        logMsg("getpkg",_cmd_rsync,1)
        run_cmd(_cmd_rsync)

        section_path=package_path+'/'+uploadPkgs
        _cmd_set_version="cd %s && echo %s >version"%(section_path,version)
        logMsg("getpkg",_cmd_set_version,1)
        run_cmd(_cmd_set_version)

        struc_modi(modi_config_file,buildHomePath)

        pkg_name=section_loop+".tar.gz"
        _cmd_tar="cd %s && tar zcvf %s %s"%(package_path,pkg_name,section_loop)
        logMsg("getpkg",_cmd_tar,1)
        run_cmd(_cmd_tar)

def scp_pkg(config_name_pkg):
    params=get_conf(config_name_pkg,"common")
    destGameSrv=params.get("destgamesrv",None)
    buildHomePath=params.get("buildhomepath",None)
    buildName=params.get("buildname",None)
    scp_source_dir=buildHomePath+'/'+buildName
    for srv_one in destGameSrv.split(","):
        cmd_scp_one="cd  %s && scp *.tar.gz qa@%s:/home/qa/deployment/build "%(scp_source_dir,srv_one)
        logMsg("getpkg",cmd_scp_one,1)
        run_cmd(cmd_scp_one)
    return True



def main():
    #print len(sys.argv)
    if len(sys.argv)!=4:
        msg="PLS input Parameter as :{.. test.ini all 1.0.1}"
        logMsg("getpkg",msg,2)
        sys.exit(1)
    else:
        config_name_pkg=sys.argv[1]
        section=sys.argv[2]
        version=sys.argv[3]

    get_build(config_name_pkg,section,version)
    # modi_config_file=get_conf(config_name_pkg,"common").get("releaseconf",None)
    # buildHomePath=get_conf(config_name_pkg,"common").get("buildhomepath",None)
    # struc_modi(modi_config_file,buildHomePath)
    scp_pkg(config_name_pkg)


if __name__=="__main__":
    main()