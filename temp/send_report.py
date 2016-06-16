#! /usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'miles.peng'
import  time,datetime
import  os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import  subprocess
import  sys
import  ConfigParser
import  logging
import boto
from pyh import *
#import signal
#import pdb

def create_files(params,section):
    datetime=str(time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time())))
    output_path=params.get("output_path",None)
    input_filename=params.get("input_filename",None)
    output_filename=params.get("output_filename",None)
    db_host=params.get("db_host",None)
    db_user=params.get("db_user",None)
    db_passwd=params.get("db_passwd",None)

    output_files=[]
    for i in range(0,len(input_filename.split(","))):
        output_filename_prefix=output_filename.split(",")[i]
        output_file="%s/%s_%s.%s"%(output_path,output_filename_prefix,datetime,"csv")
        input_file=input_filename.split(",")[i]
        input_content=read_file(input_file)

        #cmd such as :mysql -uroot -paspect -hdb_host -e"sql" >output_file
        cmd='mysql -u{0} -p{1} -h{2} -e  {3} >{4}'.format(db_user,db_passwd,db_host,input_content,output_file)
        if not run_cmd(cmd.strip('"')):
            error_msg="===%s: Create attach files Failed==="%output_file
            logging.error(error_msg)
            sys.exit(1)

        output_files.append(output_file)
    return output_files

def read_file(filename):
    with open(filename ,"r") as f:
        data=f.read()
    return data.strip("\n")


def send_mail_via_aws(params,mail_msg,_section):
    aws_id=params.get("aws_access_key_id",False)
    aws_key=params.get("aws_secret_access_key",False)

    try:
        connection=boto.connect_ses(aws_access_key_id=aws_id, aws_secret_access_key=aws_key)
        result = connection.send_raw_email(mail_msg.as_string(), source=mail_msg['from'] , destinations=mail_msg['to'].split(","))
        messageId=result.get('SendRawEmailResponse').get('SendRawEmailResult').get('MessageId')
        msg_info="Send mail %s success MessageId=%s "%(mail_msg['subject'].decode('utf-8','replace'),messageId)
        logging.info(msg_info)
        return True
    except Exception, e:
        msg_info="=== [%s] send mail via aws fail ==="%(_section)
        logging.error(msg_info)
        sys.exit(1)

def construct_mail(params,attach_files,section):
    mail_contents=params.get("mail_contents",None)
    data_is_null=params.get("is_null",None)
    msg=MIMEMultipart('alternative')
    if params.get("display_contents",None).lower()=="true":  #判断是否将查询结果作为正文展示
        html_output=create_html_contents(mail_contents,attach_files,section,data_is_null)
        html_contents=read_file(html_output)
        if html_contents:
            htm = MIMEText(html_contents,'html','utf-8')
            msg.attach(htm)
        else:
            msg="===%s: create html Failed==="%section
            logging.warn(msg)
            return False

    if params.get("include_attach",None).lower()=="true":   #判断是否将查询结构添加为附件
        for i in range(len(attach_files)):
            att = MIMEText(open(attach_files[i], 'rb').read(), 'base64', 'gb2312')
            basename = os.path.basename(attach_files[i])
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename=%s'%basename.decode('utf-8').encode('gb2312')
            msg.attach(att)

    #加邮件头
    msg['to'] =params["mail_to_list"]
    msg['from'] = params["mail_from"]
    msg['subject'] = params["mail_sub"]
    return msg

def create_html_contents(contents,attach_files,section,data_is_null):
     page = PyH('Aspect')
     mail_contents=contents.split(",")
     for i in range(len(attach_files)):
         #page<<div(style="text-align:center")<<h4(mail_contents[i])
         page<<div(style="font-weight:600")<<h4(mail_contents[i])
         mytab = page << table(border="1",cellpadding="3",cellspacing="0",style="margin:auto")
         with open(attach_files[i]) as file:
             data=file.read()
         if len(data.split("\n")) ==1:
             data=data_is_null

         #page<<div(style="text-align:center")<<h4("")

         page<<div(style="text-align:center")<<h4("\n")

         for i in range(len(data.split("\n"))):
             if data.split("\n")[i]:
                 tr2 = mytab << tr()
              #   if i != 0:
                 for j in range(len(data.split("\n")[i].split(","))):
                     tr2 << td(data.split("\n")[i].split(",")[j])
                     if i%2==0:
                         tr2.attributes['bgcolor']='#d3d3d3'
                     else:
                         tr2.attributes['bgcolor']='#c2e5c9'

         page<<div(style="text-align:center")<<h4("\n")

     dirname=os.path.dirname(attach_files[0])
     datetime=str(time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time())))
     output_file=dirname+'/'+section+'_'+datetime+'.html'
     page.printOut(output_file)
     #html=page.body
     return output_file
     #return  pag

def run_cmd(cmd):
        print "Starting run: %s "%cmd

        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        run_error=False
        out=cmdref.stderr.read()
        if out:
            run_error=True
        else:
            out = cmdref.stdout.read()
        data = cmdref.communicate()
        if cmdref.returncode == 0 and run_error==False:
            return True
        else:
            msg = "[ERROR] Run %s False \n" % cmd
            msg = msg + data[1]
            logging.warn(msg)
            logging.warn(out)
            return False

def read_conf(sections,configName):
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
     if check_conf(returnData):
        return returnData
     else:
         msg="Profile parameters do not match about %s"%sections
         logging.error(msg)
         sys.exit(1)

def check_conf(returnData):
    check_list=["mail_from","output_path","mail_to_list","mail_sub","remain_days","include_attach","db_host","db_user","db_passwd","aws_secret_access_key","aws_access_key_id"]
    input_filename=returnData.get("input_filename",None)
    output_filename=returnData.get("output_filename",None)
    mail_contents=returnData.get("mail_contents",None)

    if len(input_filename.split(",")) == len(mail_contents.split(","))==len(output_filename.split(",")):
        for check_item in check_list:
            if not returnData.get(check_item,None):
                msg="%s no found"%check_item
                logging.warn(msg)
                return False
        return True
    else:
        return False

def clear_report(TargPath,expiration):
    fileList=[]
    removeList=[]
    fileList=os.listdir(TargPath)
    for checkfile in fileList:
        filestat=os.stat(TargPath +'/'+checkfile)
        createday=datetime.date.fromtimestamp(filestat.st_atime)
        today=datetime.date.today()
        if int((today - createday).days) >= int(expiration):
            removeList.append(TargPath +'/'+ checkfile)
    if len(removeList) > 0:
        for removeFiles in removeList:
            cmd = "rm %s" % removeFiles
            if not run_cmd(cmd):
                return  False
    return True

def init_log():
    # set basic config when printing file;
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            #filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='send_report.log',
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

def write_alter(project):
    msg_info="===%s: Send Mail Failed!!==="%project
    logging.error(msg_info)
    sys.exit(1)


def main():
    configName=sys.argv[1]
    #sections为配置文件中[]内容，也为输出文件的前缀
    sections=sys.argv[2]
    init_log()
    for _section in sections.split(","):
        begin_msg="===%s: Send Mail Begin!!==="%_section
        logging.info(begin_msg)

        params=read_conf(sections=_section,configName=configName) #If read_conf failed write warn info like Get info about project Failed!! and logout with alter

        attach_files=create_files(params=params,section=_section)  #If Create attach file failed write warn info like Create attach files Failed about project and logout with alter

        if not clear_report(params["output_path"],params["remain_days"]):
            write_alter(_section)   #If clear old files failed should write cmd output in warning log and logout with alter

        if isinstance(attach_files,str):
            attach_files_list=attach_files.split(",")
        else:
            attach_files_list=attach_files

        mail_msg=construct_mail(params,attach_files_list,_section)
        if not mail_msg:
           write_alter(_section) #If Create mail failed should return "False",write message like "create html filename  Failed" in warning log,and logout with alter

        is_send=send_mail_via_aws(params,mail_msg,_section)
        if  not is_send:
            error_msg="===Config params Error==="
            logging.error(error_msg)
            sys.exit(1)
        else:
            success_msg="===%s: Send Mail Success!!==="%_section
            logging.info(success_msg)

if __name__=="__main__":
    main()