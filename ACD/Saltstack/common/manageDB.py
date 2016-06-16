#! /usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'miles.peng'


import os,sys
import pdb
from cmdrun import *
import datetime
import MySQLdb

class ManageDB(object):

    def backupDB(self,dbhost,dbuser,dbpasswd,dbname,projectname,bak_dir):
        _cmd=CmdRun()
        for _dbname in dbname:
            TargPath=bak_dir + "//" +str(projectname).strip()
            print 'Dumping %s, please wait....' % _dbname
            now=datetime.datetime.now().strftime('%Y%m%d%H%M')
            dumpFileName='%s_%s_%s.sql' % (projectname, _dbname, now)
            print dumpFileName
            cmd="/usr/bin/mysqldump -h%s -u%s -p%s %s > %s/%s" % (dbhost, dbuser, dbpasswd,_dbname,TargPath, dumpFileName)
            _cmd.run_cmd(cmd)
        return TargPath
	
    def clearBak(slef,TargPath,expiration):
        _cmd=CmdRun()
        fileList=[]
        removeList=[]
        fileList=os.listdir(TargPath)
        for checkfile in fileList:
            filestat=os.stat(TargPath +'/'+checkfile)
            createday=datetime.date.fromtimestamp(filestat.st_ctime)
            today=datetime.date.today()
            if (today - createday).days >= expiration:
                removeList.append(TargPath +'/'+ checkfile)
        if len(removeList) > 0:
            for removeFiles in removeList:
                cmd = "rm %s" % removeFiles
                _cmd.run_cmd(cmd)
        return True
	
    def sync2S3(self,bak_dir,projectName,s3_dir):
        cmd="s3cmd --delete-removed  sync  %s/ %s/%s/" % (bak_dir,s3_dir,projectName)
        _cmd=CmdRun()
        if _cmd.run_cmd(cmd):
            return  True

#such as mysql -psa -uroot -h10.1.1.60 < ~/update_db.sql
    def updateDB(self,dbhost,dbuser,dbpasswd,update_script):
        cmd="mysql -p%s -u%s -h%s < %s "%(dbpasswd,dbuser,dbhost,update_script)
        _cmd=CmdRun()
        if _cmd.run_cmd(cmd):
            return  True

    def checkDB(self,dbhost,dbuser,dbpasswd,checkDB,checkTable,dbVersion,check_sql):
        sql=check_sql%checkTable
        _values=self.sqlselect(sql,dbhost,dbuser,dbpasswd,checkDB)
        if _values[0][0].strip().lower()==str(dbVersion).strip().lower():
            print "Check DB success,Get DBVersion is %s "%_values[0][0].strip().lower()
            return
        else:
            print "[ERROR] DB Version error ,get data from DB is %s  "%_values
            sys.exit(1)


    def sqlselect(slef,sql,dbhost,dbuser,dbpasswd,checkDB):
        conn=MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpasswd,db=checkDB)
        cursor=conn.cursor()
        n=cursor.execute(sql)
        x=cursor.fetchall()
        cursor.close()
        conn.close()
        return x


def test():
    pass

if __name__ == '__main__':
    test()
