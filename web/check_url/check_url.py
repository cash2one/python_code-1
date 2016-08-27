#!/usr/bin/python
import requests
import json
import ConfigParser
import sys

import pdb
def check(url,values):
    headers = {'content-type': 'application/json'}

    s = requests.Session()
    r=s.post(url,data = json.dumps(values),headers=headers)

    the_page = r.content
    return the_page


def main():
    config_name=sys.argv[1]
    sections_=sys.argv[2]
    cf=ConfigParser.SafeConfigParser()
    cf.read(config_name)

    if sections_=="all":
        sections_=cf.sections()
    else:
        sections_=sections_.split(",")

    for section_one in sections_:
        url_=cf.get(section_one,"url")
        user_=cf.get(section_one,"user")
        passwd_=cf.get(section_one,"passwd")
        values={
                "accound": user_,
                "password": passwd_
        }
        page_info=check(url_,values)
        print "get info :", page_info

if __name__ == '__main__':
    main()
