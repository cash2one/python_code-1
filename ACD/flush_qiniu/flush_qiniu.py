#! /usr/bin/python
import requests
import json
import ConfigParser
import sys
from qiniu import  Auth, put_file,etag



def check(url,values):
    headers = {'content-type': 'application/json'}

    s = requests.Session()
    r=s.post(url,data = json.dumps(values),headers=headers)

    the_page = r.content
    return the_page

def qiniu_init(access_key,secret_key):
    q=Auth(access_key,secret_key)
    return q

def put_file(list_files,bucket_name,q):
    for file_ in list_files:
        token=q.upload_token(bucket_name,file_,3600)
        ret,info=put_file(token,file_,file_)
        print(info)
        assert ret['key'] == file_
        assert ret['hash'] == etag(file_)
    return True

def get_filename(path):
    list_files=[]

    return list_files

def main():
    cf=ConfigParser.SafeConfigParser()
    cf.read("qiniu.ini")
    access_key=cf.get("common","access_key")
    secret_key=cf.get("common","secret_key")
    put_dir=sys.argv[1]
    list_files=get_filename(put_dir)
    section=sys.argv[2]
    bucket_name=cf.get(section,"bucket_name")
    q=qiniu_init(access_key,secret_key)

    if put_file(list_files,bucket_name,q):
        print("Update %s success !"%put_dir)



if __name__ == '__main__':
    main()