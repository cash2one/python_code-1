#! /usr/bin/python

__author__ = 'william.wu'

import ConfigParser, re
import os, subprocess, logging, datetime, sys

confName = "/home/qa/scripts/AutoCreateImage/autoCreateImage.ini"
#confName = "autoCreateImage.ini"
awsCli = "/usr/local/bin/aws"
awsVars = {}
now = datetime.datetime.now()
newDate = now.strftime('%Y%m%d')

def init_log():
    # set basic config when printing file;
    """

    :rtype : object
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='/home/qa/scripts/AutoCreateImage/autoCreateImage.log',
                            #filename='autoCreateImage.log',
                            filemode='a')
        # set basic config when printing console;
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except IOError,e:
        print "Can not open log file", e
        exit(1)


def exec_cmd(command):
    try:
        shell = subprocess.Popen(command, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
    except Exception,e:
        msg = "Can not command line:",e
        logging.error(msg)
        exit(1)
    if stdout != '':
        logging.info(stdout)
        return stdout
    else:
        logging.error(stderr)
        return stderr


def create_image():
    logging.info("Start creating images...")
    for key in awsVars.iterkeys():
        args = awsVars[key].split(',')
        cmd = "%s --profile %s ec2 create-image --instance-id %s --name \"%s-%s\" --no-reboot" % (awsCli, args[0], args[1], args[2], newDate)
        logging.info(cmd)
        exec_cmd(cmd)


def delete_image():
    logging.info("Start deleting images...")
    for key in awsVars.iterkeys():
        args = awsVars[key].split(',')
        delta = now + datetime.timedelta(days=-int(args[3]))
        oldDate = delta.strftime('%Y%m%d')
        #print "delta=%s period=%s" % (delta, args[3])
        cmd = "%s ec2 --profile %s describe-images --filters \"Name=name,Values=%s-%s\"" % (awsCli, args[0], args[2], oldDate)
        logging.info(cmd)
        result = exec_cmd(cmd)
        #Get ami-id based on AMI name
        match = re.search(ur"(ami-\S+)", result)
        #delete AMI if matching image id
        if match:
            cmd = "%s ec2 --profile %s deregister-image --image-id %s" % (awsCli, args[0], match.group(0))
            logging.info(cmd)
            exec_cmd(cmd)
        else:
            logging.error("doesn't match any ami id")


def read_conf(sections):
    # read configuration and return dictionary
    conf = ConfigParser.ConfigParser()
    conf.read(confName)
    if sections == "all":
        sections = conf.sections()
    else:
        sections = sections.split(",")
    for secs in sections:
        instanceID = conf.get(secs, "instanceID")
        imageName = conf.get(secs, "name")
        profile = conf.get(secs, "profile")
        periodOfReserve = conf.getint(secs, "periodofreserve")
        awsVars[secs] = "%s,%s,%s,%d" % (profile, instanceID, imageName, periodOfReserve)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print len(sys.argv)
        print "Usages: %s [all|sections]" % sys.argv[0]
        sys.exit(1)
    section = sys.argv[1]
    read_conf(section)
    init_log()
    logging.info("-------------------Staring-------------------------")
    create_image()
    delete_image()
    logging.info("-------------------Ending-------------------------")