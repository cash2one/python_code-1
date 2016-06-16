#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__ = 'miles.peng'

import sys,subprocess,re
import time
import ConfigParser
import logging
import pdb

#CurrTime = time.strftime('%Y-%m-%d_%H:%M', time.localtime(time.time()))
def init_log():
    # set basic config when printing file;
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='/home/qa/miles/log/modiconf.log',
                            filemode='a')
        # set basic config when printing console;
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except IOError,e:
        print "Can't open log file", e
        exit(1)

class Modiconfig():

  def change_conf(self,conFileName,sourData,targData):
        #pdb.set_trace()
        cmd="sed -i '/%s/Is#=.*$#%s#' %s" %('^'+sourData.strip()+'=',('='+targData),conFileName)
#        print cmd
#        logging.info(cmd)
    #    pdb.set_trace()
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            buff = p.stdout.readline()
            if buff == '':
                break
            else:
                if p.poll()==0:
                    logger.info(buff)
                else:
                    logger.error(buff)
                    sys.exit(1)

  def read_conf(self,fileName,sectionName):
        cf=ConfigParser.ConfigParser()
        cf.read(fileName)
        ConfigDataSection=cf.sections()
        sectionsName=[]
        commonSourData=[]
        commonTargData=[]
        conFileName=""
        returnData={}

    #    pdb.set_trace()
        #get common date useing in all files
        if "common" in ConfigDataSection:
            commonAllData=cf.items("common")
            ConfigDataSection.remove("common")
            for a,b in commonAllData:
                commonSourData.append(a)
                commonTargData.append(b)

        #check filename which need modify by sectionName
        if sectionName.lower()== "all":
            sectionsName=ConfigDataSection
        else:
            for _sectionName in ConfigDataSection:
                if sectionName in _sectionName:
                    sectionsName.append(_sectionName)

        if len(sectionsName)==0:
            exit(1)

        #get source,target by conf file for each file
        for _section in sectionsName:
            itemData = cf.items(_section)
            sectionSourData=[]
            sectionTargData=[]

            for modiSource,modiTarget in itemData:
                sectionSourData.append(modiSource)
                sectionTargData.append(modiTarget)

            for _length in range(len(commonSourData)):
                sectionSourData.append(commonSourData[_length])
                sectionTargData.append(commonTargData[_length])

            conFileName=_section
            #pdb.set_trace()
            if len(commonSourData) != len(commonTargData):
                msg= "Please check config files content ,source Data length isn`t same as Targer Data"
                print msg
                exit(1)
            else:
                #return one files modofy parameters like dict[a] = {listSource,listTarget}
                returnData[conFileName]=(sectionSourData,sectionTargData)

        return returnData

if __name__ == "__main__":
    argNum = len(sys.argv)
    if argNum < 3:
#    if argNum != 3:
        message = "Parameter is :{Config files Path&Name}"
        print message
        exit(1)
    fileName=sys.argv[1]
    sectionName=sys.argv[2]
    init_log() 
    logger=logging.getLogger('main')
    newConfig=Modiconfig()
#    logger.info("-------------------Staring-------------------------")  
    print "    |__ Start modify configuration"
    returnData=newConfig.read_conf(fileName.split(),sectionName)
    if returnData == {}:
        print "[ERROR] No files need modify"
        sys.exit(1)
    #pdb.set_trace()
    for conFileName in returnData:
        (sectionSourData,sectionTargData)=returnData[conFileName]
        for _len in range(len(sectionSourData)):
            newConfig.change_conf(conFileName,sectionSourData[_len],sectionTargData[_len])
#    logger.info("-------------------Ending-------------------------")  
    print "    |__ Stop modify configuration"