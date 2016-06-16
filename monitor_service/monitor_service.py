#!/usr/bin/python

import ConfigParser
import logging
import subprocess
import time
import sys
import os
import pdb

def run_cmd(cmd,output=False):
    print "Starting run: %s "%cmd
    cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out=cmdref.stdout.read()
    if output:
        return out.strip("\n")
    else:
        return True


def _init_log():
       # set basic config when printing file;
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='monitor_service.log',
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

def get_config(filename,values):
     cf=ConfigParser.SafeConfigParser()
     sections=values
     cf.read(filename)
     configDataSection=cf.sections()
     returnData={}

     if sections in configDataSection:
         _list=cf.items(sections)
         for _key,_value in _list:
             returnData[_key]=_value
     else:
         print "[ERROR] %s is not in config files,PLS check it %s" %(sections,filename)
         msg_info="===%s: Get info Failed!!==="%sections
         logging.error(msg_info)
         sys.exit(1)

     return returnData


def get_hostname():
    sys = os.name
    if sys == 'nt':
            hostname = os.getenv('computername')
            return hostname

    elif sys == 'posix':
            host = os.popen("hostname")
            try:
                    hostname = host.read()
                    return hostname.strip("\n")
            finally:
                    host.close()
    else:
            return 'Unkwon hostname'


def _check_service(key):
    _run=key

    if run_cmd(_run,output=True):
        return  True
    return False

def _start_service(key):
    _run=key
    if run_cmd(_run):
        return  True
    return False

def main():
    _init_log()
    host=get_hostname()
    print host
    host_file="host_service.ini"
    service_file="service_info.ini"
    sleep_time=10
    param_services=get_config(host_file,host)
    services=param_services.get("service",None).split(",")
    need_start=[]
    for service in services:
        param=get_config(service_file,service)
        _service=param.get("check_service",None)
        if not _check_service(_service):
            need_start.append(service)

    if not need_start:
        msg="No service need restart"
        logging.info(msg)
        sys.exit(0)
    else:
        for _err_service in need_start:
            _err_param=get_config(service_file,_err_service)
            retry=_err_param.get("retry",None)
            start_service=_err_param.get("start_service",None)
            check_service=_err_param.get("check_service",None)
            i=0
            while 1:
                _start_service(start_service)
                time.sleep(sleep_time)
                if _check_service(check_service):
                    msg="Start service %s Success!!"%_err_service
                    logging.info(msg)
                    break
                else:
                    i=i+1
                    msg="check service %s %s Failed!!"%(_err_service,i)
                    logging.warn(msg)
                    if i==int(retry):
                        msg="Start service %s ERROR"%_err_service
                        logging.error(msg)
                        sys.exit(1)


if __name__=="__main__":
    main()