#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import sys
import qiniu
import ConfigParser
import logging
import os
import boto3

'''
This script for upload to S3(boto) or qiniu,
start like "upload_resources.py config_files project_name version(which was number of dest_path)"
First check config file ,get upload method (s3 or qiniu ),source_path,dest_path
second check source_path get files which neen to upload to a list
as method run upload_s3 or qiniu to upload
'''
log_file="default.log"

def get_upload_files(dir):
    list_files=[]
    if not os.path.isdir(dir):
        msg="%s is not a directory ,PLS check it "%dir
        logMsg("get upload files",msg,2)
        sys.exit(1)

    for root,dirs,files in os.walk(dir):
        if files:
            get_files=(root,files)
            list_files.append(get_files)

    return list_files

def upload_s3():
    pass

def upload_qiniu():
    pass

def initlog():
    import logging
    logger = None
    logger = logging.getLogger()
    hdlr = logging.FileHandler(log_file)
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
    logger.removeHandler( hdlr )
    #logMsg("modify",cmd_sed,1)


def main(config_file,project_name,version):
    cf=ConfigParser.SafeConfigParser()
    cf.read(config_file)
    source_path=cf.get(project_name,"upload_path")
    list_files=get_upload_files(source_path)
    upload_method=cf.get(project_name,"method")

    if upload_method.lower()=="s3":
        bucket_name=cf.get(project_name,"bucket_name")
        target_path=cf.get(project_name,"target_path")
        target_path_prefix=("%s/%s/%s")%(bucket_name,target_path,version)
        s3_access_key_id=cf.get("common","s3_access_key_id")
        s3_secret_access_key=cf.get("common","s3_secret_access_key")
        if upload_s3(list_files,target_path_prefix,s3_access_key_id,s3_secret_access_key):
            msg="upload %s  success"%project_name
            logMsg("upload_s3",msg,1)

    elif upload_method.lower()=="qiniu":
        bucket_name=cf.get(project_name,"bucket_name")
        target_path=cf.get(project_name,"target_path")
        target_path_prefix=("%s/%s/%s")%(bucket_name,target_path,version)
        qiniu_access_key_id=cf.get("common","qiniu_access_key_id")
        qiniu_secret_access_key=cf.get("common","qiniu_secret_access_key")
        if upload_qiniu(list_files,target_path_prefix,qiniu_access_key_id,qiniu_secret_access_key):
            msg="upload %s  success"%project_name
            logMsg("upload_qiniu",msg,1)
    else:
        msg="Method %s not define "%upload_method.lower()
        logMsg("upload",msg,2)
        sys.exit(1)


if __name__=="__main__":
    if len(sys.argv)!=4:
        print "Start parameter error ,must like upload_resources.py config_files project_name version ! "
        sys.exit(1)

    config_file=sys.argv[1]
    project_name=sys.argv[2]
    version=sys.argv[3]

    main(config_file,project_name,version)