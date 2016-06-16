#!/usr/bin/python
# coding=utf8
from __future__ import division
__author__ = 'jerry.liu'
import ConfigParser
import datetime
import sys
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
from email.header import Header
import pdb

def sendmail(to_list,host,me,subject,files,content,sysbl):
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		filename='/home/qa/scripts/sendReport/goldpay/GoldpayReportSendmail.log',
		filemode='a+')
	mail_list = to_list.split(';')
	for i in mail_list:
		msg = MIMEMultipart()
		h = Header('Goldpay')
		h.append('<'+me+'>')
		msg['From'] = h
	        msg['To'] = i
		msg['Subject'] = subject
		msg['Date'] = formatdate(localtime=True)
		msg.attach(MIMEText(content,'html','utf8'))
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(files, 'rb').read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(files))
		msg.attach(part)
        	smtp = smtplib.SMTP(host)
		smtp.set_debuglevel(1)
		try:
			smtp.sendmail(me,i,msg.as_string())
			logging.info('%s %s email send success.' % (sysbl,i))
			print 'email send success.'
		except Exception ,e:
			logging.error('%s %s email send failed. %s' % (sysbl,i,e))  
        		print e  
        		print 'email send failed.'
		smtp.quit()
	
def getcontentsys():
	now = datetime.datetime.now()
	now_strf = now.strftime('%Y/%m/%d')
	delta_1 = delta=datetime.timedelta(days=1)
	delta_8 = delta=datetime.timedelta(days=8)
	now_1 = now - delta_1
	now_8 = now - delta_8
	now_1_strf = now_1.strftime('%Y-%m-%d')
	report_time = now_1.strftime('%Y/%m/%d')
	report_time_1 = now_1.strftime('%Y.%m.%d')
	now_8_strf = now_8.strftime('%Y-%m-%d')
	f = open('/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_System_Report_%s.html' % report_time_1,'a+')

	f.write('<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Goldpay Daily System Report %s</title></head><body>' % report_time)
	f.write(' <table width=100%% height="209" border="1"  cellspacing="0" cellpadding="0" ><col width=20%% /><col width=10%% /><col width=10%% /><col width=10%% /><col width=10%% /><col width=10%% /><col width=10%% /><col width=10%% /><col width=10%% />')

	f.write('<caption align="top">Goldpay Daily System Report '+report_time+'</caption>')
	
	f.write('<tr><td width=20%%></td>')
	f.write('<td width=10%%>'+now_1_strf+'</td>')
	f.write('<td width=10%%>Wow</td>')
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y.%m.%d')
		f.write('<td width=10%%>'+sqltime_strf+'</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>New Users</td>')
	sql_1 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE create_at  >=\''+now_1_strf+' 00:00:00\' AND create_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_1 = os.popen(sql_1)
	cmdstr_1 = cmd_1.read()
	f.write('<td width=10%%>'+cmdstr_1+'</td>')
	sql_1_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE create_at  >=\''+now_8_strf+' 00:00:00\' AND create_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_1_8 = os.popen(sql_1_8)
	cmdstr_1_8 = cmd_1_8.read()
	if int(cmdstr_1_8) != 0:
		wow_1 = (int(cmdstr_1)-int(cmdstr_1_8))/int(cmdstr_1_8)*100
	else:
		wow_1 = (int(cmdstr_1)-int(cmdstr_1_8))*100
	if wow_1 < 0:
		f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_1,2))
	else:
		f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_1,2))
	for j in range(2,8):
		delta=datetime.timedelta(days=j)
		sqltime = now - delta
		sqltime_strf = sqltime.strftime('%Y-%m-%d')
		sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE create_at  >=\''+sqltime_strf+' 00:00:00\' AND create_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
		cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
			f.write('<td width=10%%>'+cmdstr+'</td>')
		else:
			f.write('<td width=10%%>0</td>')
	f.write('</tr>')	

	f.write('<tr><td width=20%%>Total Users</td>')
	sql_2 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE user_type !=\'1\' AND  create_at<=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_2 = os.popen(sql_2)
        cmdstr_2 = cmd_2.read()
	f.write('<td width=10%%>'+cmdstr_2+'</td>')
	sql_2_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE user_type !=\'1\' AND  create_at<=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_2_8 = os.popen(sql_2_8)
	cmdstr_2_8 = cmd_2_8.read()
	if int(cmdstr_2_8) != 0:
		wow_2 = (int(cmdstr_2)-int(cmdstr_2_8))/int(cmdstr_2_8)*100
	else:
		wow_2 = (int(cmdstr_2)-int(cmdstr_2_8))*100
	if wow_2 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_2,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_2,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta 
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(*) FROM goldq_user WHERE user_type !=\'1\' AND  create_at<=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                	f.write('<td width=10%%>'+cmdstr+'</td>')
		else:
			f.write('<td width=10%%>0</td>')
	f.write('</tr>')

	f.write('<tr><td width=20%%>Total Trans Created</td>')
	sql_3 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' OR order_status=\'created\') AND create_at >=\''+now_1_strf+' 00:00:00\' AND create_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_3 = os.popen(sql_3)
	cmdstr_3 = cmd_3.read()
	f.write('<td width=10%%>'+cmdstr_3+'</td>')
	sql_3_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' OR order_status=\'created\') AND create_at >=\''+now_8_strf+' 00:00:00\' AND create_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_3_8 = os.popen(sql_3_8)
	cmdstr_3_8 = cmd_3_8.read()
	if int(cmdstr_3_8) != 0:
		wow_3 = (int(cmdstr_3)-int(cmdstr_3_8))/int(cmdstr_3_8)*100
	else:
		wow_3 = (int(cmdstr_3)-int(cmdstr_3_8))*100
	if wow_3 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_3,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_3,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' OR order_status=\'created\') AND create_at >=\''+sqltime_strf+' 00:00:00\' AND create_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
                cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>Success Trans Cnt</td>')
	sql_4 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' ) AND create_at >=\''+now_1_strf+' 00:00:00\' AND create_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_4 = os.popen(sql_4)
	cmdstr_4 = cmd_4.read()
	f.write('<td width=10%%>'+cmdstr_4+'</td>')
	sql_4_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' ) AND create_at >=\''+now_8_strf+' 00:00:00\' AND create_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_4_8 = os.popen(sql_4_8)
	cmdstr_4_8 = cmd_4_8.read()
	if int(cmdstr_4_8) != 0:
		wow_4 = (int(cmdstr_4)-int(cmdstr_4_8))/int(cmdstr_4_8)*100
	else:
		wow_4 = (int(cmdstr_4)-int(cmdstr_4_8))*100
        if wow_4 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_4,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_4,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_order WHERE (order_status=\'completed\' ) AND create_at >=\''+sqltime_strf+' 00:00:00\' AND create_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>Success Trans Amt</td>')
	sql_5 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT SUM(balance) FROM  goldq_order WHERE (order_status=\'completed\' ) AND complete_at  >=\''+now_1_strf+' 00:00:00\' AND complete_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_5 = os.popen(sql_5)
	cmdstr_5 = cmd_5.read()
	if cmdstr_5.strip() == 'NULL':
		cmdstr_5 = '0'
        f.write('<td width=10%%>'+cmdstr_5+'</td>')
	sql_5_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT SUM(balance) FROM  goldq_order WHERE (order_status=\'completed\' ) AND complete_at  >=\''+now_8_strf+' 00:00:00\' AND complete_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_5_8 = os.popen(sql_5_8)
        cmdstr_5_8 = cmd_5_8.read()
	if cmdstr_5_8.strip() != 'NULL' and int(cmdstr_5_8) != 0:
        	wow_5 = (int(cmdstr_5)-int(cmdstr_5_8))/int(cmdstr_5_8)*100
	elif cmdstr_5_8.strip() == 'NULL':
		wow_5 = int(cmdstr_5)*100
	else:
		wow_5 = (int(cmdstr_5)-int(cmdstr_5_8))*100
        if wow_5 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_5,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_5,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT SUM(balance) FROM  goldq_order WHERE (order_status=\'completed\' ) AND complete_at  >=\''+sqltime_strf+' 00:00:00\' AND complete_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>Android Trans Cnt</td>')
	sql_6 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'android\' AND complete_at  >=\''+now_1_strf+' 00:00:00\' AND complete_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_6 = os.popen(sql_6)
        cmdstr_6 = cmd_6.read()
        f.write('<td width=10%%>'+cmdstr_6+'</td>')
	sql_6_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'android\' AND complete_at  >=\''+now_8_strf+' 00:00:00\' AND complete_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_6_8 = os.popen(sql_6_8)
        cmdstr_6_8 = cmd_6_8.read()
	if int(cmdstr_6_8) != 0:
        	wow_6 = (int(cmdstr_6)-int(cmdstr_6_8))/int(cmdstr_6_8)*100
	else:
		wow_6 = (int(cmdstr_6)-int(cmdstr_6_8))*100
        if wow_6 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_6,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_6,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'android\' AND complete_at  >=\''+sqltime_strf+' 00:00:00\' AND complete_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>iOS Trans Cnt</td>')
	sql_7 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'ios\' AND complete_at  >=\''+now_1_strf+' 00:00:00\' AND complete_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_7 = os.popen(sql_7)
        cmdstr_7 = cmd_7.read()
        f.write('<td width=10%%>'+cmdstr_7+'</td>')
	sql_7_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'ios\' AND complete_at  >=\''+now_8_strf+' 00:00:00\' AND complete_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_7_8 = os.popen(sql_7_8)
        cmdstr_7_8 = cmd_7_8.read()
	if int(cmdstr_7_8) != 0:
        	wow_7 = (int(cmdstr_7)-int(cmdstr_7_8))/int(cmdstr_7_8)*100
	else:
		wow_7 = (int(cmdstr_7)-int(cmdstr_7_8))*100
        if wow_7 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_7,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_7,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'ios\' AND complete_at  >=\''+sqltime_strf+' 00:00:00\' AND complete_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>Web Trans Cnt</td>')
	sql_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'web\' AND complete_at  >=\''+now_1_strf+' 00:00:00\' AND complete_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_8 = os.popen(sql_8)
        cmdstr_8 = cmd_8.read()
        f.write('<td width=10%%>'+cmdstr_8+'</td>')
	sql_8_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'web\' AND complete_at  >=\''+now_8_strf+' 00:00:00\' AND complete_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_8_8 = os.popen(sql_8_8)
        cmdstr_8_8 = cmd_8_8.read()
	if int(cmdstr_8_8) != 0:
        	wow_8 = (int(cmdstr_8)-int(cmdstr_8_8))/int(cmdstr_8_8)*100
	else:
		wow_8 = (int(cmdstr_8)-int(cmdstr_8_8))*100
        if wow_8 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_8,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_8,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_type =\'web\' AND complete_at  >=\''+sqltime_strf+' 00:00:00\' AND complete_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>Fee Trans Cnt</td>')
	sql_9 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_bill_seq WHERE (status=\'completed\') AND create_at >=\''+now_1_strf+' 00:00:00\' AND create_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_9 = os.popen(sql_9)
        cmdstr_9 = cmd_9.read()
        f.write('<td width=10%%>'+cmdstr_9+'</td>')
	sql_9_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_bill_seq WHERE (status=\'completed\') AND create_at >=\''+now_8_strf+' 00:00:00\' AND create_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_9_8 = os.popen(sql_9_8)
        cmdstr_9_8 = cmd_9_8.read()
	if int(cmdstr_9_8) != 0:
        	wow_9 = (int(cmdstr_9)-int(cmdstr_9_8))/int(cmdstr_9_8)*100
	else:
		wow_9 = (int(cmdstr_9)-int(cmdstr_9_8))*100
        if wow_9 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_9,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_9,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id) FROM  goldq_bill_seq WHERE (status=\'completed\') AND create_at >=\''+sqltime_strf+' 00:00:00\' AND create_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')

	f.write('<tr><td width=20%%>CRM Trans Cnt</td>')
	sql_10 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_info =\'CRM_TRANS_OUT\' AND complete_at  >=\''+now_1_strf+' 00:00:00\' AND complete_at <=\''+now_1_strf+' 23:59:59\';"|tail -1'
	cmd_10 = os.popen(sql_10)
        cmdstr_10 = cmd_10.read()
        f.write('<td width=10%%>'+cmdstr_10+'</td>')
	sql_10_8 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_info =\'CRM_TRANS_OUT\' AND complete_at  >=\''+now_8_strf+' 00:00:00\' AND complete_at <=\''+now_8_strf+' 23:59:59\';"|tail -1'
	cmd_10_8 = os.popen(sql_10_8)
        cmdstr_10_8 = cmd_10_8.read()
	if int(cmdstr_10_8) != 0:
        	wow_10 = (int(cmdstr_10)-int(cmdstr_10_8))/int(cmdstr_10_8)*100
	else:
		wow_10 = (int(cmdstr_10)-int(cmdstr_10_8))*100
        if wow_10 < 0:
                f.write('<td width=10%%><font color="#FF0000">%s%%</font></td>' % round(wow_10,2))
        else:
                f.write('<td width=10%%><font color="##00CC66">%s%%</font></td>' % round(wow_10,2))
	for j in range(2,8):
                delta=datetime.timedelta(days=j)
                sqltime = now - delta
                sqltime_strf = sqltime.strftime('%Y-%m-%d')
                sql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e "SELECT COUNT(DISTINCT id)  FROM  goldq_order WHERE (order_status=\'completed\') AND   order_info =\'CRM_TRANS_OUT\' AND complete_at  >=\''+sqltime_strf+' 00:00:00\' AND complete_at <=\''+sqltime_strf+' 23:59:59\';"|tail -1'
		cmd = os.popen(sql)
                cmdstr = cmd.read()
		if cmdstr.strip() != 'NULL':
                        f.write('<td width=10%%>'+cmdstr+'</td>')
                else:
                        f.write('<td width=10%%>0</td>')
        f.write('</tr>')
	
	f.write('</table></body></html>')
	f.close()


def getcontentbl():
	now = datetime.datetime.now()
	delta_1 = delta=datetime.timedelta(days=1)
	now_1 = now - delta_1
	report_time = now_1.strftime('%Y/%m/%d')
	report_time_1 = now_1.strftime('%Y.%m.%d')
	f = open('/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.csv.1' % report_time_1,'a+')	
	h = open('/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.html' % report_time_1,'a+')
	h.write('<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Goldpay Daily Balance Report %s</title></head><body><table cellspacing="0" cellpadding="0" border="1"><col width="183" /><col width="126" /><col width="72" /><col width="110" /><col width="96" /><caption align="top">Goldpay Daily Balance Report %s</caption><tr><td width="183">日期</td><td width="126">会员名</td><td width="72">账号类型</td><td width="110">账号</td><td width="96">金蛋余额</td></tr>' % (report_time,report_time))
	
	h.write('<tr>')
	f.write('日期,会员名,账号类型,账号,金蛋余额\n')
	cmd_1 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e \'SELECT "%s" AS "日期",goldq_crm_admin.admin_name AS "会员名",goldq_user.user_type AS "账号类型",goldq_crm_account.account_id  AS "账号",SUM(goldq_crm_account.balance) AS "金蛋余额" FROM goldq_crm_account,goldq_crm_admin,goldq_user  WHERE goldq_crm_account.user_id =goldq_crm_admin.id AND goldq_user.user_type=\'1\' GROUP BY goldq_crm_account.account_type\'|tail -n +2' % report_time
	cmd_exec_1 = os.popen(cmd_1)
	list_1 = cmd_exec_1.read().split()
	for i in range(0,5):
		if i == 2:
			list_1[i] = '系统账号'
		if i == 4:
			h.write('<td align="right">%s</td>' % list_1[i])
			f.write('%s\n' % list_1[i])
		else:
			h.write('<td>%s</td>' % list_1[i])
			f.write('%s,' % list_1[i])
	h.write('</tr>')

	h.write('<tr>')
	cmd_2 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e \'SELECT "%s" AS "日期",goldq_user.username AS "会员名",goldq_user.user_type AS "账号类型",goldq_crm_account.account_id  AS "账号",SUM(goldq_crm_account.balance) AS "金蛋余额" FROM goldq_crm_account,goldq_user WHERE goldq_crm_account.user_id IN (SELECT id  FROM  goldq_user WHERE user_type=\'9\') AND goldq_user.user_type=\'9\' GROUP BY goldq_crm_account.account_type\'|tail -n +2' % report_time
	cmd_exec_2 = os.popen(cmd_2)
	list_2 = cmd_exec_2.read().split()
	for j in range(0,5):
		if j == 2:
                        list_2[j] = '手续费'
                if j == 4:
                        h.write('<td align="right">%s</td>' % list_2[j])
			f.write('%s\n' % list_2[j])
                else:
                        h.write('<td>%s</td>' % list_2[j])
			f.write('%s,' % list_2[j])
        h.write('</tr>')

	cmd_3 = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e \'SELECT "%s" AS "日期",temp2.username AS "会员名", temp2.user_type AS "账号类型", temp1.account_id AS "账号", temp1.balance AS "金蛋余额" FROM (SELECT id, username,user_type FROM goldq_user WHERE user_type=\'2\' OR user_type=\'3\')temp2 LEFT JOIN (SELECT balance,account_id,user_id FROM goldq_account) temp1   ON temp1.user_id=temp2.id\'|tail -n +2' % report_time
	cmd_exec_3 = os.popen(cmd_3)
	for line in cmd_exec_3.readlines():
		list_3 = line.split()
		h.write('<tr>')
		for m in range(0,5):
			if m == 2:
				list_3[m] = '个人'
                	if m == 4:
                        	h.write('<td align="right">%s</td>' % list_3[m])
				f.write('%s' % list_3[m])
                	else:
                        	h.write('<td>%s</td>' % list_3[m])
				f.write('%s,' % list_3[m])
		h.write('</tr>')
		f.write('\n')
	
	eggsql = 'mysql -hprod-goldpay.ccp7bt1yxa0k.ap-southeast-1.rds.amazonaws.com -uroot -paspectqa -Dprod-goldpay -e \'SELECT balance FROM goldq_crm_account WHERE account_id="163587600023"\'|tail -n +2'
	totaleggs = os.popen(eggsql).read()
	h.write(' <tr><td colspan="3" width="381" align="right">金蛋总数：</td><td colspan="2" width="206" align="right">%s</td></tr></table></body></html>' % totaleggs)
	f.write('金蛋总数：, %s' % totaleggs)
if __name__ == '__main__':
	if  len(sys.argv) != 2:
		print 'Usage: <yourscript> <option>'
        	print "   option: sys"
		print "           bl "
        	exit(1)
	now = datetime.datetime.now()
	delta = datetime.timedelta(days=1)
	delta_2 = datetime.timedelta(days=2)
	now_1 = now - delta
	now_2 = now - delta_2
	now_1_strf = now_1.strftime('%Y.%m.%d')
	now_2_strf = now_2.strftime('%Y.%m.%d')
	host = '127.0.0.1'
	me = 'no-reply@goldpay.com'
#        pdb.set_trace()
	if len(sys.argv) == 2:
		config = ConfigParser.ConfigParser()
    		config.readfp(open('/home/qa/scripts/sendReport/goldpay/GoldpayReportSendmail.ini','rb'))
		if sys.argv[1] == 'sys':
			sysbl = 'sys'
			to_list = config.get('SystemMailTo','mailtolist')
			subject = 'Goldpay Daily System Report %s' % now_1_strf
			files = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_System_Report_%s.html' % now_1_strf
			files_2 = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_System_Report_%s.html' % now_2_strf
			if os.path.exists(files):
				os.remove(files)
			if os.path.exists(files_2):
                                os.remove(files_2)
			getcontentsys()
			content = open(files,'rb').read()
			sendmail(to_list,host,me,subject,files,content,sysbl)
		elif sys.argv[1] == 'bl':
			sysbl = 'bl'
			to_list = config.get('BalanceMailTo','mailtolist')
			subject = 'Goldpay Daily Balance Report %s' % now_1_strf
			files = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.csv' % now_1_strf
			files_csv1 = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.csv.1' % now_1_strf
			files_html = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.html' % now_1_strf
			files_2 = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.csv' % now_2_strf
			files_2_csv1 = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.csv.1' % now_2_strf
			files_html_2 = '/home/qa/scripts/sendReport/goldpay/report/Goldpay_Daily_Balance_Report_%s.html' % now_2_strf
			os.system('/bin/rm -f %s %s %s %s %s %s' % (files,files_csv1,files_html,files_2,files_2_csv1,files_html_2))
			getcontentbl()
			os.system('/usr/bin/iconv -f UTF-8 -t GB2312 ' +files_csv1+ ' > ' +files)
			content = open(files_html,'rb').read()
			sendmail(to_list,host,me,subject,files,content,sysbl)
		else:
			print 'Usage: <yourscript> [sys|bl]'
