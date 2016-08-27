#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

import sys
import subprocess
import ConfigParser
import time


def _run_cmd(cmd,_is_dubeg):
    print "Starting run: %s "%cmd
    if _is_dubeg:
        return True
    else:
        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error_info = cmdref.communicate()
        if error_info:
            print "RUN ERROR,error info:  ",error_info
            return False
        else:
            print "Run Output:\t",output
            return True


def splic_command(cf,sections):
    file_pipe=[]
    service_pipe=[]
    source_path=cf.get("common","source_path")
    bak_path=cf.get("common","bak_path")
    bastion_ip=cf.get("common","bastion_ip")
    bastion_path=cf.get("common","bastion_path")


    #删除“common”标签
    if "common" in sections:
        sections.remove("common")

    for section in sections:
        #检查各模块中有无“dest_path”设置，如有存在覆盖"common"中的配置
        keys_=dict(cf.items(section)).keys()
        if "dest_path" in keys_:
            dest_path=cf.get(section,"dest_path")
        else:
            dest_path=cf.get("common","dest_path")

        bak_name="{0}/{1}{2}".format(bak_path,section,time.strftime("%Y%m%d",time.localtime()))
        update_file="{0}/{1}".format(source_path,section)

        scp_cmd="scp qa@{0}:{1}/{2}.tar.gz {3}/. ".format(bastion_ip,bastion_path,section,source_path)
        file_pipe.append("{6} &&cd {0} && tar zxvf {1}.tar.gz && cd {2} && mv {3} {4} && cp -r {5} .".format(source_path,section,dest_path,section,bak_name,update_file,scp_cmd))

        service_pipe.append(cf.get(section,"start_cmd"))

    #过滤重复的命令
    service_pip_deduplication=list(set(service_pipe))
    if "" in service_pip_deduplication:
        service_pip_deduplication.remove("")

    return file_pipe,service_pip_deduplication



def main():
    #
    config_file=sys.argv[1]
    sections_p=sys.argv[2]
    if len(sys.argv)==4 and sys.argv[3].lower()=="test":
        _is_dubeg=True
    else:
        _is_dubeg=False

    cf=ConfigParser.SafeConfigParser()
    cf.read(config_file)

    if sections_p.lower()=="all":
        sections=cf.sections()
    else:
        sections=sections_p.split(",")

    file_pipe,service_pipe=splic_command(cf,sections)

    for file_pipe_cmd in file_pipe:
        _run_cmd(file_pipe_cmd,_is_dubeg)

    for service_pipe_cmd in service_pipe:
        _run_cmd(service_pipe_cmd,_is_dubeg)
        time.sleep(6)


if __name__=="__main__":
    main()

