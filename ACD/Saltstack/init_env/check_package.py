#!/usr/bin/python
__author__ = 'miles.peng'
Root_dir="/srv/salt/deploy_workflow"
import sys
sys.path.append(Root_dir)
import sys
from ACD.tools.deploy_code.make_pkg import common


#from deploy_workflow import Root_dir


def check_package(check_host,get_version_cmd,package_version):
    cmd='salt "%s" cmd.run "%s"'%(check_host,get_version_cmd)
    _cmdrun= common.cmdrun.CmdRun()
    out=_cmdrun.run_salt_package_check(cmd)
    check_out=out.splitlines()[-1].strip()
    #print "Check host=%s cmd=%s output is %s,input version is %s"%(check_host,get_version_cmd,check_out,package_version)
    if check_out.strip().lower()!=package_version.lower():
        print "get version not == package_version %s %s"%(check_out.strip().lower(),package_version.lower())
        return False
    else:
        print "Remote host package is same as define"
        return True


def install_package(check_host,install_sls,package_filename,package_dir,user):
    cmd="sudo salt '%s' state.sls sls.%s pillar='{package_dir: '%s', package_filename: '%s',user: '%s'}'"%(check_host,install_sls,package_dir,package_filename,user)
    salt_mode = "state"
    _cmdrun= common.cmdrun.CmdRun()
    if _cmdrun.run_salt(cmd,salt_mode):
        return  True
    else:
        return False

def install_pkg(check_host,install_sls,pkg_name):
    cmd="sudo salt '%s' state.sls sls.%s pillar='{pkg_name: '%s'}'"%(check_host,install_sls,pkg_name)
    salt_mode = "state"
    _cmdrun= common.cmdrun.CmdRun()
    if _cmdrun.run_salt(cmd,salt_mode):
        return  True
    else:
        return False



def check_service(check_host,check_service_cmd):
    cmd='salt "%s" cmd.run "%s"'%(check_host,check_service_cmd)
    _cmdrun= common.cmdrun.CmdRun()
    out=_cmdrun.run_salt_package_check(cmd)
    if not out:
        return True
    else:
        return False




def check_workflow(projectName,SectionName,check_host_list):
    check_section_filename=Root_dir+"/init_env/section_package.ini"
    check_package_filename=Root_dir+"/init_env/packages.ini"
    section="%s-%s"%(projectName,SectionName)
    _config= common.configparser.Getconfig()
    _packages=_config.getconfig(section,check_section_filename)["packages"]
    packages=_packages.split(",")
#    check_host_list=[]
#   if not hostName:
#       workflow_ini=Root_dir+"/ini/"+projectName+"_workflow.ini"
#       hosts=_config.getconfig(SectionName,workflow_ini)["host"]
#       for host_parallel in hosts.split("|"):
#           for host_serial in host_parallel.split(","):
#               check_host_list.append(host_serial)
#   else:
#       check_host_list=hostName.split(",")

    for check_host in check_host_list:
        for package in packages:
            _check_info=_config.getconfig(package,check_package_filename)
            package_version=_check_info["package_version"]
            get_version_cmd=_check_info["get_version_cmd"]
            if not check_package(check_host,get_version_cmd,package_version):
                check_service_cmd=_check_info["check_service_cmd"]
                if not check_service(check_host,check_service_cmd):
                    install_mode=_check_info["install_mode"]
                    if install_mode.strip().lower()=="apt_get":
                        if _check_info["install_sls"] and _check_info["pkg_name"]:
                            install_sls=_check_info["install_sls"]
                            pkg_name=_check_info["pkg_name"]
                            if install_pkg(check_host,install_sls,pkg_name):
                                print "%s %s install via pkg mode success \n"%(check_host,pkg_name)
                                return True
                        else:
                            print "Some parameters undefined \n"
                            sys.exit(1)
                    elif install_mode.strip().lower()=="package":
                        if _check_info["package_filename"] and _check_info["package_dir"] and _check_info["install_sls"] and _check_info["user"] :
                            install_sls=_check_info["install_sls"]
                            package_filename=_check_info["package_filename"]
                            package_dir=_check_info["package_dir"]
                            user=_check_info["user"]
                            if install_package(check_host,install_sls,package_filename,package_dir,user):
                                 print "%s %s install via package mode success \n"%(check_host,package_filename)
                                 #return True
                        else:
                            print "Some parameters undefined "
                            sys.exit(1)
                    else:
                        print "install_mode defined error"
                        sys.exit(1)
                else:
                    print "%s need Updated but it`s working \n"%package
    return  True


def init_user_dir(check_host_list):
    for host in check_host_list:
        cmd='salt "%s" state.sls sls.deploy_init'%host
        salt_mode = "state"
        _runcmd= common.cmdrun.CmdRun()
        if _runcmd.run_salt(cmd,salt_mode):
            print "Initialization user dir etc success \n"
            return  True
        else:
            print "[ERROR] Init User/Dir Failed"
            return  False


def get_hostname(projectName,SectionName,hostName):
    _config= common.configparser.Getconfig()
    check_host_list=[]
    if not hostName:
        workflow_ini=Root_dir+"/ini/"+projectName+"_workflow.ini"
        hosts=_config.getconfig(SectionName,workflow_ini)["host"]
        for host_parallel in hosts.split("|"):
            for host_serial in host_parallel.split(","):
                check_host_list.append(host_serial)
    else:
        check_host_list=hostName.split(",")
    return check_host_list






def check_main(projectName,SectionName,hostName=None):
    check_host_list=get_hostname(projectName,SectionName,hostName)
    init_user_dir(check_host_list)
    if check_workflow(projectName,SectionName,check_host_list):
        print("==================Check package success=====================")
        return True
    else:
        return False

#   install_list=check_workflow(projectName,SectionName,hostName)
#   if install_list:
#       for user,package_name,install_cmd,install_dir in install_list:
#           install_package(user,package_name,install_cmd,install_dir)
#       re_check=check_workflow(projectName,SectionName,hostName)
#       if re_check:
#           print "[ERROR] Something install Failed ,PLS check it"
#           sys.exit(1)
#       else:
#           print "Check package sucessful"
#           return  True
#   else:
#       print "Check package sucessful Nothing need install "
#       return  True








if __name__=="__main__":
    print "=================Begin Check Packages========================"
    if len(sys.argv)!=4:
        print "Pls input like %s ProjectName SectionName HostName"%sys.argv[0]
        sys.exit(1)
    projectName=sys.argv[1]
    SectionName=sys.argv[2]
    hostName=sys.argv[3]
    if check_main(projectName,SectionName,hostName):
        print "==================Check END=========================="

