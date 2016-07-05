import os
import sys

def test():
    CMD_RUN=__salt__['cmd.run']
    cmd="ls /etc/init.d"
    return CMD_RUN(cmd)

def myscript(*t,**kv):
    ret=__salt__['cmd.script'](*t,**kv)
    print ret
    return ret

def check_Service(servername):
    CMD_RUN=__salt__['cmd.run']
    cmd="ps -ef|grep %s |grep -v grep|grep -c %s" % (servername,servername)
#    cmd='ps -ef |more '
    out=CMD_RUN(cmd,python_shell=True)
    return out

def get_files_info(filename):
    cmd="cat %s" % filename
    CMD_RUN=__salt__['cmd.run']
    out=CMD_RUN(cmd,python_shell=True)
    return out
