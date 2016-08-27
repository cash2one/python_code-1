#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import ansible.runner
import json


def getHostinfoByName(hostname):
	files_ini='/home/qa/miles/script/ansible/vm.ini'
	runner=ansible.runner.Runner(host_list=files_ini,module_name='setup'\
	                             ,pattern=hostname)
	output=runner.run()
	
	hostinfo=dict()
	hostinfo['mem']=output['contacted'][hostname]['ansible_facts']['ansible_memory_mb']['real']['total']
	hostinfo['os_verson']="%s %s"%(output['contacted'][hostname]['ansible_facts']['ansible_distribution']\
	            ,output['contacted'][hostname]['ansible_facts']['ansible_distribution_version'])
	ips=output['contacted'][hostname]['ansible_facts']['ansible_all_ipv4_addresses']
	priv_ip_l=[]
	pub_ip_l=[]
	for ip in ips.split(','):
		if str(ip.split('.')[0]) in ['172','192','10'] :
			priv_ip_l.append(ip)
		else:
			pub_ip_l.append(ip)
	hostinfo['priv_ip']=priv_ip_l
	hostinfo['pub_ip']=pub_ip_l
	
	return hostinfo
			
			
def mainProcess(hostname):
	hostinfo=getHostinfoByName(hostname)


if __name__=="__main__":
	hostname='vm02'
	mainProcess(hostname)
