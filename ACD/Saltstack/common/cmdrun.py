#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import logging
import sys
import pdb
# __author__ = 'miles.peng'
'''命令行调用通用方法'''



class CmdRun():

    def run_cmd(self, cmd):
        print "Starting run: %s "%cmd
        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = cmdref.stdout.read()
        print "run cmd  output "+out
        data = cmdref.communicate()
        if cmdref.returncode == 0:
            msg = "Run %s success \n" % cmd
            msg = msg + data[0]
            print(msg)

            return True
        else:
            msg = "[ERROR] Run %s False \n" % cmd
            msg = msg + data[1]
            print msg

            sys.exit(1)
            return False


# 基于SLS的命令行调用方法，并对返回值进行判断
#section like this
# ['Test-GOC-Game-SrvB01:', '----------', '          ID: puttaskserver', '    Function: file.managed', '        Name: //etc/init.d/taskserver', '      Result: True', '     Comment: File //etc/init.d/taskserver is in the correct state', '     Started: 09:17:39.215021', '    Duration: 179.338 ms', '     Changes:   ', '----------', '          ID: puttomcat', '    Function: file.managed', '        Name: //etc/init.d/tomcat', '      Result: True', '     Comment: File //etc/init.d/tomcat is in the correct state', '     Started: 09:17:39.395861', '    Duration: 178.775 ms', '     Changes:   ', '', 'Summary', '------------', 'Succeeded: 2', 'Failed:    0', '------------', 'Total states run:     2', 'Test-Guest-Game-Srv:', '----------', '          ID: puttaskserver', '    Function: file.managed', '        Name: //etc/init.d/taskserver', '      Result: True', '     Comment: File //etc/init.d/taskserver updated', '     Started: ', '    Duration: ', '     Changes:   ', '              ----------', '              diff:', '                  New file', '              group:', '                  qa', '              mode:', '                  755', '              user:', '                  qa', '----------', '          ID: puttomcat', '    Function: file.managed', '        Name: //etc/init.d/tomcat', '      Result: True', '     Comment: File //etc/init.d/tomcat updated', '     Started: ', '    Duration: ', '     Changes:   ', '              ----------', '              diff:', '                  New file', '              group:', '                  qa', '              mode:', '                  755', '              user:', '                  qa', '', 'Summary', '------------', 'Succeeded: 2 (changed=2)', 'Failed:    0', '------------', 'Total states run:     2', 'Test-Game-Srv:', '----------', '          ID: puttaskserver', '    Function: file.managed', '        Name: //etc/init.d/taskserver', '      Result: True', '     Comment: File //etc/init.d/taskserver updated', '     Started: 09:17:54.550472', '    Duration: 919.416 ms', '     Changes:   ', '              ----------', '              diff:', '                  New file', '              group:', '                  qa', '              mode:', '                  0755', '              user:', '                  qa', '----------', '          ID: puttomcat', '    Function: file.managed', '        Name: //etc/init.d/tomcat', '      Result: True', '     Comment: File //etc/init.d/tomcat updated', '     Started: 09:17:55.471412', '    Duration: 759.124 ms', '     Changes:   ', '              ----------', '              diff:', '                  New file', '              group:', '                  qa', '              mode:', '                  0755', '              user:', '                  qa', '', 'Summary', '------------', 'Succeeded: 2 (changed=2)', 'Failed:    0', '------------', 'Total states run:     2', '']



    def run_salt(self, cmd, salt_mode):
        #print "--------------------Starting run_salt-------------------------"

        #print cmd


        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = cmdref.stdout.read()

        #Saltstack执行结果输出开关
        #print "output is %s" %out
        if out == "" or "ERROR " in out:
            print "[ERROR] Saltstack script run Failed"
            sys.exit(1)
        if salt_mode == "state":
            if "Failed:" not in out:
                print "[ERROR] Salt return error output is %s" % out
                sys.exit(1)

            for checkline in out.split("\n"):
                if "Failed:" in checkline:
                    checkdata = checkline.split(":")[-1].strip()
                    if checkdata != str(0):
                        print "[ERROR] Salt out find error output is %s" % out
                        sys.exit(1)


        elif salt_mode == "module":
            for i in range(len(out.split("\n"))):
                _mod = i % 2
                if _mod == 1:
                    if out.split("\n")[i].strip() != "True":
                        print "[ERROR] %s return Error Values is %s" % (out.split("\n")[i - 1], out.split("\n")[i].strip())
                        sys.exit(1)

        #msg="End run_salt:"+cmd
        #print "--------------------End run_salt-------------------------------"
        return True


    #执行自定义方法，返回结果
    def run_salt_out(self, cmd):
        #print "-----------------Start run_salt_out----------------------"
        #print cmd

        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = cmdref.stdout.read().splitlines()[-1].strip()
        #print out
        data = cmdref.communicate()
        if cmdref.returncode == 0:
            return out
        else:
            print("[ERROR] Run salt cmd error %s") % cmd
            sys.exit(1)

        #print "----------------------End run_salt_out %s ----------------------------"
        return True

    def run_salt_package_check(self, cmd):
        print "---------------------Start check service---------------------"
        print cmd
        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out=cmdref.stdout.read()
        return out
