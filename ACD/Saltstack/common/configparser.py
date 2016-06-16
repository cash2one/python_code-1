#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'miles.peng'
import  ConfigParser
import  sys
import pdb
'''按输入projectname解析对应的配置文件，并将相应数据以dict方式返回'''
class Getconfig():


    def getconfig(self,sections,configName):

        cf=ConfigParser.ConfigParser()
        cf.read(configName)
        configDataSection=cf.sections()
        returnData={}
        if sections in configDataSection:
            _list=cf.items(sections)
            for _key,_value in _list:
                returnData[_key]=_value
        else:
            print "[ERROR] %s is not in config files,PLS check it %s" %(sections,configName)
            sys.exit(1)
        return returnData







