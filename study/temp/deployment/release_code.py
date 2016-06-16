#!/usr/bin/python
import ConfigParser
import subprocess
import sys
import logging
import time

def init_log():
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='release_code.log',
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

def get_config(sections,configName):
     cf=ConfigParser.SafeConfigParser()
     cf.read(configName)
     configDataSection=cf.sections()
     returnData={}
     _common=cf.items("common")

     for _common_key,_common_value in _common:
         returnData[_common_key]=_common_value

     if sections in configDataSection:
         _list=cf.items(sections)
         for _key,_value in _list:
             returnData[_key]=_value
     else:
         print "[ERROR] %s is not in config files,PLS check it %s" %(sections,configName)
         msg_info="===%s: Get info Failed!!==="%sections
         logging.error(msg_info)
         sys.exit(1)
     return  returnData

def run_cmd(cmd):
     print "Starting run: %s "%cmd
     # cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
     # run_error=False
     # out=cmdref.stderr.read()
     # if out:
     #     run_error=True
     # else:
     #     out = cmdref.stdout.read()
     # data = cmdref.communicate()
     # if cmdref.returncode == 0 and run_error==False:
     #     return True
     # else:
     #     msg = "[ERROR] Run %s False \n" % cmd
     #     msg = msg + data[1]
     #     logging.warn(msg)
     #     logging.warn(out)
     #     return False

def make_cmd(_section,_values):
    source_path=_values.get("source_path","/home/qa/deployment/build")
    bak_path=_values.get("bak_path",None)
    dest_path=_values.get("dest_path",None)
    start_cmd=_values.get("start_cmd",None)

    bak_name="{0}/{1}{2}".format(bak_path,_section,time.strftime("%Y%m%d",time.localtime()))
    new_file="{0}/{1}".format(source_path,_section)

    release_file_cmd="cd {0} && tar zxvf {1} && cd {2} && mv {3} {4} && cp -r {5} .".format(source_path,_section,dest_path,_section,bak_name,new_file)

    return release_file_cmd,start_cmd


def main():
    configName=sys.argv[1]
    input_sections=sys.argv[2]
    msg="==================Starting=============="
    logging.info(msg)
    if  input_sections=="all":
        cf=ConfigParser.SafeConfigParser()
        cf.read(configName)
        sections=cf.sections()
        
        sections.remove("common")
    else:
        sections=input_sections.split(",")

    service_cmd=list()

    #clear source_path


    for section in sections:
        config_value=get_config(section,configName)
        release_file_cmd,start_cmd=make_cmd(section,config_value)
        run_cmd(release_file_cmd)
        service_cmd.append(start_cmd)

    service_cmd_deduplication=list(set(service_cmd))
    if "" in service_cmd_deduplication:
        service_cmd_deduplication.remove("")

    for service_run in service_cmd_deduplication:
        run_cmd(service_run)
        time.sleep(5)


    msg="=====================relases complete====================="
    logging.info(msg)


if __name__=="__main__":
    main()

