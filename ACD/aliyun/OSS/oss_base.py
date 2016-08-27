#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

import oss2

def list_bucket(auth,endpoint):
    service = oss2.Service(auth, endpoint)
    print([b.name for b in oss2.BucketIterator(service)])
    return True


def login(keyid,secureid):
    auth = oss2.Auth(keyid, secureid)
    return auth

def _get_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com"):
    bucket = oss2.Bucket(auth, url,bucket_name)
    return bucket


def create_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com"):
    bucket=_get_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com")
    bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)

def upload(auth,bucket_name,remote_file,local_file,url="http://oss-cn-hangzhou.aliyuncs.com"):
    bucket=_get_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com")
    bucket.put_object_from_file(remote_file, local_file)

def download(auth,bucket_name,remote_file,local_file,url="http://oss-cn-hangzhou.aliyuncs.com"):
    bucket=_get_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com")
    bucket.get_object_to_file(remote_file, local_file)

def list_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com"):
    from itertools import islice
    bucket=_get_bucket(auth,bucket_name,url="http://oss-cn-hangzhou.aliyuncs.com")
    for b in islice(oss2.ObjectIterator(bucket), 10):
        print(b.key)



if __name__=="__main__":
    remote_file="/tmp/test"
    local_file="/data/test"
    keyid="123"
    secureid="343"
    bucket_name="test"

    auth=login(keyid,secureid)
    upload(auth,bucket_name,remote_file,local_file,url="http://oss-cn-hangzhou.aliyuncs.com")