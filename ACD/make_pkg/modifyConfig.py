#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__ = 'miles.peng'


from common import  *

#

def modi_conf(modi_filename,source,dest):
    if not os.path.isfile(modi_filename):
        msg="%s file can`t find,Nothing can`t do!"%modi_filename
        logMsg("modify",msg,2)
        return True
       # sys.exit(1)
    for len_ in range(len(source)):
        cmd_sed="sed -i '/%s/Is#=.*$#%s#' %s" %('^'+source[len_].strip()+'=',('='+dest[len_]),modi_filename)
        logMsg("modify",cmd_sed,1)
        run_cmd(cmd_sed)
    return True

def struc_modi(filename):
    #init_log("modify.log")
    cf=ConfigParser.SafeConfigParser()
    cf.read(filename)
    section_=cf.sections()
    if "common" in section_:
        section_.remove("common")
    for section_one in section_:

        returnData=get_conf(filename,section_one)
        source=returnData.keys()
        dest=returnData.values()
        change_file=section_one
        modi_conf(change_file,source,dest)
    return True

if __name__=="__main__":
    filename=sys.argv[1]
    struc_modi(filename)