#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import docker
import ConfigParser
import commands
import sys

def initlog():
    import logging
    logger = None
    logger = logging.getLogger()
    hdlr = logging.FileHandler("default.log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return [logger,hdlr]

def logMsg( fun_name, err_msg,level ):
    message = fun_name + ':'+err_msg
    logger,hdlr = initlog()
    logger.log(level ,message )
    hdlr.flush()
    logger.removeHandler( hdlr )#网络上的实现基本为说明这条语句的使用和作用


def get_conf(filename,section):
    cf=ConfigParser.SafeConfigParser()
    cf.read(filename)
    returnData={}
    if "common" in cf.sections():
        _data_default=cf.items("common")
        for _common_key,_common_value in _data_default:
            returnData[_common_key]=_common_value

    _data=cf.items(section)
    if not _data:
        msg="Get Values about %s in config file %s ERROR"%(section,filename)
        #print msg
        logMsg("common",msg,1)
        #logging.error("Get Values about %s in config file %s ERROR")%(section,filename)
        sys.exit(1)
    for _key,_value in _data:
         returnData[_key]=_value
    return returnData

def run_cmd(cmd):
    (status, result)=commands.getstatusoutput(cmd)
    if status !=0:
        print result
        sys.exit(1)
    else:
        success_msg="Run cmd:%s success \n "%cmd
        print success_msg
        return True

def get_host():
    import socket
    hostname=socket.gethostname()
    while 1:
        if hostname[-1] in "1234567890":
            hostname=hostname[0:-1]
        else:
            return hostname


def check_docker(docker_list):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    docker_infos=cli.containers()
    for docker_ in docker_list.split(","):
        for docker_info in docker_infos:
            is_check=False
            if docker_info["Names"].lower()==docker_.lower():
                is_check=True
                if docker_info["State"] != u'running':
                    start_docer(docker_info["Names"])
            if is_check==False:
                msg="Docker %s not found"%docker_info["Names"]
                logMsg("check",msg,2)
                return False
    return True


def start_docer(name):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    cli.start(container=name)
    return True

def main():
    filename_ini=sys.argv[1]
    host_name=get_host()
    check_data=get_conf(filename_ini,host_name)
    docker_list=check_data.get("docker_names",None)
    if check_docker(docker_list):
        msg="check all docker are running"
        logMsg("SUCCESS",msg,1)
    else:
        msg="check docker Faild"
        logMsg("ERROR",msg,2)


if __name__=="__main__":
    main()

