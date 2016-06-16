#! /usr/bin/python

import requests
import json
from qiniu import  Auth

def check(url,values):
    headers = {'content-type': 'application/json'}

    # headers={
    #     "X-Requested-With": "XMLHttpRequest",
    #     "Accept": "application/json, text/javascript, */*; q=0.01",
    #     "Access-Control-Allow-Origin": "*",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36",
    #     "Connection": "keep-alive",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Content-Length": "65",
    #     "Content-Type": "application/json;charset=utf-8"
    # }
    #pdb.set_trace()
    s = requests.Session()
    r=s.post(url,data = json.dumps(values),headers=headers)
    #r=requests.post(url,data=json.dumps(values),headers=headers)

    the_page = r.content
    return the_page

def main():
    url ="http:://fusion.qiniuapi.com/refresh"
    access_key= "pL738cMCowEfEIliey3iR6kl9bP1rdpk5dGrZfoQ"
    secret_key="bCMffocLKb3Q_L9LkJGNtO1qUpN0tX1RSVrT7MmP"
    q=Auth(access_key,secret_key)

    #//fusion.qiniuapi.com/refresh"
    values={
    "accound":"yuantest003@sina.com",
    "password":"12345678"
    }
    page_info=check(url,values)
   # pdb.set_trace()
    print page_info

if __name__ == '__main__':
    main()