#!/usr/bin/python
import boto.ses
import re
import datetime
import sys
import ConfigParser
import pdb

def check_ses(region,aws_access_key_id,aws_secret_access_key):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
#    pdb.set_trace()
    conn = boto.ses.connect_to_region(
        region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    jsonOutput = conn.get_send_statistics()
    todayList = []

    for i in  jsonOutput['GetSendStatisticsResponse']['GetSendStatisticsResult']['SendDataPoints']:
        if re.search(today,i['Timestamp']):
            todayList.append(i)

    todayList.sort(key=lambda todayListSort : todayListSort['Timestamp'])

    if int(todayList[-1:][0]['DeliveryAttempts']) != 0:
        wow = round(int(todayList[-1:][0]['Bounces'])/int(todayList[-1:][0]['DeliveryAttempts']), 2)
    else:
        wow = 0

    return str(wow).strip()

def get_config(filename):
    cf=ConfigParser.ConfigParser()
    cf.read(filename)
    configSection=cf.sections()
    returnData={}

    for section in configSection:
        sectionData={}
        itemData=cf.items(section)
        for a,b in itemData:
            sectionData[a]=b
        returnData[section]=sectionData
        del sectionData

    return returnData

def main():
    checkData=get_config("getSesStatistics.ini")
    for task_name in checkData.keys():
        region=checkData[task_name].get("region","Null")
        aws_access_key_id=checkData[task_name].get("aws_access_key_id","Null")
        aws_secret_access_key=checkData[task_name].get("aws_secret_access_key","Null")
        if region and aws_access_key_id and aws_secret_access_key:
            wow=check_ses(region,aws_access_key_id,aws_secret_access_key)
            outFile=task_name+'.log'
            with open(outFile,'w') as files:
                files.write(wow)
        else:
            print "Get config from files ERROR"
            sys.exit(1)

if __name__=="__main__":
    main()

