#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import os
import sys
import pdb
import subprocess

def filter_file(dir,param):
    check_files=[]
    if os.path.isdir(dir):
        for root,dirs,files in os.walk(dir):
            for file in files:
                if file.split(".")[-1] in param:
                    check_files.append(os.path.join(root,file))
    return check_files

def remove_nouse(check_files,nouse):
    import copy
    check_files_new=copy.deepcopy(check_files)
    for nouse_one in nouse:
        for check_file in check_files:
            # print "check file :",check_file
            if nouse_one in check_file:
                # print "remove file :",check_file
                check_files_new.remove(check_file)

    # for aa in check_files:
    #     print "check_start: ",aa
    # for a in check_files_new:
    #     print "check_end: ",a
    return check_files_new


def diff_files(check_files,sour_dir,dest_dir):
    check_output=dict()
    for check_file_source in check_files:
        check_file_dest=check_file_source.replace(sour_dir,dest_dir)
        #     _is_diff,diff_text=diff_text_check(check_file_source,check_file_dest)
        cmd="diff -Nrcab %s %s"%(check_file_source,check_file_dest)
        _is_diff,diff_text=_run(cmd)
        if _is_diff:
             check_output[check_file_source]=diff_text
    return check_output



def _run(cmd):
        cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output,error_info = cmdref.communicate()
        if error_info:
            print "ERROR output was: ",error_info
            sys.exit(1)
            #return False,error_info

        else:
            return True,output




def remove_note(data):
    new_data=[]
    for line_ in data:
        if line_.strip() and line_.strip()[0]!="#" :
            new_data.append(line_.strip())
    return new_data


def diff_text_check(source,dest):
    diff_text=[]
    _is_diff=False
    with open(source) as f1:
        data_source=f1.read().split("\n")
    data_source_remove=remove_note(data_source)

    if not os.path.isfile(dest):
        pdb.set_trace()
        _is_diff=True
        msg="%s file no found!!"%dest
        diff_text.append(msg)
        return _is_diff,diff_text

    with open(dest) as f2:
        data_dest=f2.read().split("\n")
    data_dest_remoce=remove_note(data_dest)

    if len(data_source_remove)==len(data_dest_remoce):
        for line_source in data_source_remove:
            if line_source not  in data_dest_remoce:
                _is_diff=True
                diff_text.append(line_source)
        return _is_diff,diff_text
    else:
        pdb.set_trace()
        _is_diff=True
        diff_text.append("Source length isn`t same as Dest")
        return _is_diff,diff_text


def main():
    param=["js","properties"]
    sour_dir=sys.argv[1]
    dest_dir=sys.argv[2]
    check_files=filter_file(sour_dir,param)
    nouse=["test","dev","production"]

    check_files=remove_nouse(check_files,nouse)
    check_output=diff_files(check_files,sour_dir,dest_dir)
    for keys_,values_ in check_output.items():
        if values_:
            print "diff filenames: ",keys_
            print values_

    # if check_output:
    #     for key_ in check_output.keys():
    #         print "diff filename :",key_
    #         for line_ in check_output[key_]:
    #             print "\t Source:",line_

if __name__=="__main__":
    main()