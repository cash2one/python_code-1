#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import sys

class test(object):
    def __init__(self,key):
        self.key=key
        self.Model="Post"

    @classmethod
    def check_model(self):
        if self.Model=="Post":
            self.Model="Get"
        else:
            self.Model="Unknow"

    def print_a(self):
        staticmethod(check_model)
        print "Class method A:",self.Model


    def print_b(self):
        staticmethod(check_model)
        print "Class method B:",self.Model


