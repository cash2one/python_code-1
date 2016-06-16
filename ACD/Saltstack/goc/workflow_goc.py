__author__ = 'miles.peng'

from workflow.workflow_salt import *
class Goc():

    def check_section_version_goc(self,_host,check_section,sectionVersion):
        _workflow=Workflow_salt()
        if _workflow.remot_check_version(host,check_section,sectionVersion):
            print "Check host=%s %s = %s success"%(host,check_section,sectionVersion)
            return True