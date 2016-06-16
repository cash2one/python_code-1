#!/usr/bin/python
import  ConfigParser
import  commands
import sys
import logging
import pdb

def init_log():
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='db_manager.log',
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

def db_backup(param):
    dbuser=param.get("dbuser",None)
    dbpasswd=param.get("dbpasswd",None)
    dbhost=param.get("dbhost",None)
    output_path=param.get("output_path",None)
    tiggers=param.get("tiggers",None)
    filenames=param.get("filenames",None)

    tigger_l=tiggers.split(",")
    filenames_l=filenames.split(",")
    for i in range(len(tigger_l)):
        pdb.set_trace()
        full_name=output_path+'/'+filenames_l[i]
        cmd="mysqldump -u%s -p%s --single-transaction --order-by-primary -h%s --triggers %s > %s"%(dbuser,dbpasswd,dbhost,tigger_l[i],full_name)
        log_msg="db backup cmd is %s"%cmd
        logging.info(log_msg)
        (status, result)=commands.getstatusoutput(cmd)
        if status !=0:
            error_msg="Run cmd ERROR! error code=%s \n %s"%(str(status),result)
            logging.error(error_msg)
            sys.exit(1)
        else:
            success_msg="Run cmd success %s"%result
            logging.info(success_msg)
    return True

def db_run(param):
    dbuser=param.get("dbuser",None)
    dbpasswd=param.get("dbpasswd",None)
    dbhost=param.get("dbhost",None)
    sql=param.get("sql",None)
    cmd="mysql -p%s -u%s -h%s -e%s "%(dbpasswd,dbuser,dbhost,sql)
    (status, result)=commands.getstatusoutput(cmd)
    if status !=0:
        logging.error("Run cmd ERROR!")
        sys.exit(1)
    else:
        success_msg="Run cmd success \n %s"%result
        logging.info(success_msg)
    return True

def db_restore(param):
    dbuser=param.get("dbuser",None)
    dbpasswd=param.get("dbpasswd",None)
    dbhost=param.get("dbhost",None)
    input_path=param.get("input_path",None)
    filenames=param.get("filenames",None)
    tiggers=param.get("tiggers",None)

    filename_l=filenames.split(",")
    tigger_l=tiggers.split(",")
    for i in range(len(filename_l)):
        full_name=input_path+'/'+filename_l[i]
        cmd="mysql -u%s -p%s -h%s -A %s < %s"%(dbuser,dbpasswd,dbhost,tigger_l[i],full_name)
        log_msg="db restore cmd is %s"%cmd
        logging.info(log_msg)
        (status, result)=commands.getstatusoutput(cmd)
        if status !=0:
            error_msg="Run cmd ERROR! error code=%s \n %s"%(str(status),result)
            logging.error(error_msg)
            sys.exit(1)
        else:
            success_msg="Run cmd success %s"%result
            logging.info(success_msg)
    return True

def main():
    init_log()
    if not sys.argv[1]:
        logging.error("PLS input config file name")
        sys.exit(1)
    elif not sys.argv[2]:
        logging.error("PLS input function list like backup,restor!")
        sys.exit(1)
    else:
        logging.info("==========================Begin==================")

    config_name=sys.argv[1]
    run_lists=sys.argv[2].split(",")
    for run_list in run_lists:
        param=get_conf(config_name,run_list)
        eval(run_list)(param)
    logging.info("====================End===============================")

if __name__=="__main__":
    main()



