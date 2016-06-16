#! /usr/bin/python

import requests
import json
from qiniu import  Auth, put_file,etag

access_key= "pL738cMCowEfEIliey3iR6kl9bP1rdpk5dGrZfoQ"
secret_key="bCMffocLKb3Q_L9LkJGNtO1qUpN0tX1RSVrT7MmP"

def check(url,values):
    headers = {'content-type': 'application/json'}

    s = requests.Session()
    r=s.post(url,data = json.dumps(values),headers=headers)

    the_page = r.content
    return the_page

def qiniu_init(access_key,secret_key):
    q=Auth(access_key,secret_key)
    return q

def put_file(d_file,q):

    bucket_name = d_file.get("bucket_name")    #要上传的空间
    key = d_file.get("dest_filename")              #上传到七牛后保存的文件名
    #policy={    'callbackUrl':'http://your.domain.com/callback.php',
    #'callbackBody':'filename=$(fname)&filesize=$(fsize)'
    # }

    #token = q.upload_token(bucket_name, key, 3600,policy)       #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    localfile = d_file.get("sour_filename")     #要上传文件的本地路径

    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)       #  上传&回调


def main():
    q=qiniu_init(access_key,secret_key)



if __name__ == '__main__':
    main()