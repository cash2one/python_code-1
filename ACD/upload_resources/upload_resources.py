#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import sys
import ConfigParser
import logging
import json
import pdb

'''
This script for upload to S3(boto) or qiniu,
start like "upload_resources.py config_files project_name version(which was number of dest_path)"
First check config file ,get upload method (s3 or qiniu ),source_path,dest_path
second check source_path get files which neen to upload to a list
as method run upload_s3 or qiniu to upload
request awscli&qrsync
'''
log_file="default.log"


def upload_s3(source_path,target_path_prefix,profile):
    cmd="aws s3 sync {source_path} {target_path}  --acl public-read --cache-control='no-cache' " \
        "--profile {profile}".format(source_path=source_path,target_path=target_path_prefix,profile=profile)
    if _run(cmd):
        msg="upload {source_path} success!".format(source_path=source_path)
        logMsg("S3",msg,1)
        print msg
    return True

def upload_qiniu_qshell(qiniu_dict,version):
     source=qiniu_dict.get("src_dir",None)
     cmd="sh /home/qa/miles/scripts/ACD/upload_resources/remove_tmp.sh {source} {version}".format(source=source,version=version)
     upload_path='/tmp/qiniu/'
     if _run(cmd):
         json_template={
             "src_dir"   : upload_path,
                 "access_key":   qiniu_dict["qiniu_access_key"],
                "secret_key":   qiniu_dict["qiniu_secret_key"],
                "bucket"    :   qiniu_dict["bucket_name"],
                "up_host"   :   "http://upload.qiniu.com",
                "ignore_dir":   False,
                "rescan_local": True,
                "key_prefix":  qiniu_dict.get("key_prefix",""),
                "overwrite" :   False,
                "check_exists" : False
         }
         with open("/tmp/qiniu.conf",'w') as f:
             f.write(json.dumps(json_template,indent=4))

         sync_cmd="/home/qa/miles/qiniu/qshell qupload 10 /tmp/qiniu.conf"
         if _run(sync_cmd):
             msg="Sync {source} to {dest} success".format(source=upload_path,dest=qiniu_dict["bucket_name"])
             logMsg("Qiniu",msg,1)
             print "Sync complete"


def initlog():
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

def _run(cmd):
    import subprocess
    cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output,error_info = cmdref.communicate()
    if error_info:
        msg= "RUN %s ERROR,error info: %s "%(cmd,error_info)
        print msg
        logMsg("cmd",msg,2)
        return False
    else:
        print "Run %s Success!! \n %s"%(cmd,output)
        return True



def main(config_file,project_name,version):
    cf=ConfigParser.SafeConfigParser()
    cf.read(config_file)
    source_path=cf.get(project_name,"source_path")
    upload_method=cf.get(project_name,"upload_method")

    if upload_method.lower()=="s3":
        target_path=cf.get(project_name,"target_path")
        profile=cf.get(project_name,"profile")
        target_path_prefix=("%s/%s")%(target_path,version)
        upload_s3(source_path,target_path_prefix,profile)


    elif upload_method.lower()=="qiniu":
        qiniu_dict=dict()
        qiniu_dict["src_dir"]=source_path
        qiniu_dict["qiniu_access_key"]=cf.get(project_name,"qiniu_access_key")
        qiniu_dict["qiniu_secret_key"]=cf.get(project_name,"qiniu_secret_key")
        qiniu_dict["bucket_name"]=cf.get(project_name,"bucket_name")

        if upload_qiniu_qshell(qiniu_dict,version):
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