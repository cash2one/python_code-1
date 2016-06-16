#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wayne.zhang'

import logging
import sys,re
import ConfigParser

def init_log():
    # set basic config when printing file;
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='/tmp/getPkgs.log',
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

def read_conf(fileName,sectionName):
        cf=ConfigParser.ConfigParser()
        cf.read(fileName)
        ConfigDataSection=cf.sections()
        print "ConfigDataSection:",ConfigDataSection

if __name__ == "__main__":
        argNum = len(sys.argv)
        if argNum < 4:
            message = "Usage: getPkgs.pl [project name] [section name in project file] [version]\n  e.g: getPkgs.pl goc all v1.1.1\n"
            print message
            exit(1)
        projectName=sys.argv[1]
        sectionName=sys.argv[2]
        moduleVer=sys.argv[3]
        init_log()
        fileName=projectName+'_getPkgs.ini'
        read_conf(fileName,sectionName)
