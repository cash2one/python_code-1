#!/usr/bin/python
import os
import sys
import logging
import modifyConfig
import commands
import ConfigParser

def init_log():
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='get_pkg.log',
                            filemode='a')
        # set basic config when printing console;
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except IOError,e:
        print "Can't open log file", e
        sys.exit(1)

def get_conf(filename,section):
    cf=ConfigParser.SafeConfigParser()
    cf.read(filename)
    returnData={}
    _data=cf.items(section)
    if not _data:
        logging.error("Get Values about %s in config file %s ERROR")%(section,filename)
        sys.exit(1)
    for _key,_value in _data:
         returnData[_key]=_value
    return returnData

def run_cmd(cmd):
    (status, result)=commands.getstatusoutput(cmd)
    if status !=0:
        logging.error("Run cmd ERROR!")
        sys.exit(1)
    else:
        success_msg="Run cmd success \n %s"%result
        logging.info(success_msg)
        return True

def get_build(config_name_pkg,section,version):
    if section == "all":
        section_get_collect=get_conf(config_name_pkg,"DEFAULT").get("include",None)
        if section_get_collect:
            section_collect=section_get_collect.split(",")
        else:
            msg="include no found!"
            logging.error(msg)
            sys.exit(1)
    else:
        section_collect=section.split(",")

    #clear build dir
    default_param=get_conf(config_name_pkg,"DEFAULT")
    buildHomePath=default_param.get("buildHomePath",None)
    buildName=default_param.get("buildName",None)
    build_path=buildHomePath+'/packages/'
    cmd="cd %s && rm -r %s && mkdir -p %s"%(build_path,buildName,buildName)
    run_cmd(cmd)

    package_path=build_path+buildName
    for section_loop in section_collect:
        _param=get_conf(config_name_pkg,section_loop)
        srcGameSrv=_param.get("srcGameSrv",None)
        rsyncTagPath=_param.get("rsyncTagPath",None)
        uploadPkgs=_param.get("uploadPkgs",None)
        #as "rsync -vzrtopg --delete --progress qa@54.223.79.251::DeploymentHome/apache-tomcat/webapps/rollit_html/ ./rollit_html"
        _cmd="cd %s && rsync -vzrtopg --delete --progress qa@%s::%s/%s/ ./%s"%(package_path,srcGameSrv,rsyncTagPath,uploadPkgs,uploadPkgs)
        run_cmd(_cmd)

        section_path=package_path+'/'+'uploadPkgs'
        _cmd="cd %s && echo %s >version"%(section_path,version)
        run_cmd(_cmd)



def modify_conf():
    pass

def make_gz():
    pass



def main():
    init_log()
    if len(sys.argv)!=3:
        msg="PLS input Parameter as :{.. test.ini all 1.0.1}"
        logging.error(msg)
        sys.exit(1)
    else:
        config_name_pkg=sys.argv[1]
        section=sys.argv[2]
        version=sys.argv[3]

    get_build(config_name_pkg,section,version)
    modify_conf()
    make_gz()






if __name__=="__main__":
    main()