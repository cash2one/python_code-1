#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = 'Miles Peng'


import sys
import logging
import commands
import ConfigParser

git_dir=["/srv/salt/deploy_workflow/conf","/srv/salt/deploy_workflow/ini","/srv/salt/deploy_workflow/common"]

def init_log(log_file="default.log"):
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename=log_file,
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

def _run_cmd(cmd):
    print cmd
    return True