#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

from sqlalchemy import Column,String,create_engine,Integer,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

conn_str="'mysql://root:aspect@172.18.188.147/aspect',convert_unicode=True,echo=True,encoding='utf8'"

def db_connect(conn_str):
    engine = create_engine(conn_str)
    DBSession=sessionmaker(bind=engine)
    session=DBSession()
    return session

#def __insert(session,values_):


class Hostlist(Base):
    __tablename__='hostlist'

    id=Column(Integer,primary_key=True,autoincrement =True)
    vir_id=Column(String(20))
    priv_ip=Column(String(20))
    #info=relationship("Hostinfo")

    def __init__(self,vir_id,priv_ip):
        self.vir_id=vir_id
        self.priv_ip=priv_ip

    def __repr__(self):
        return "<Hostlist('%s','%s')>"%(self.vir_id,self.priv_ip)


def get_virtual_id(self):
    import uuid
    return str(uuid.uuid4())

class Hostinfo(Base):
    __tablename__="hostinfo"
    id=Column(Integer,primary_key=True,autoincrement =True)
    vir_id=Column(String(20))
    hostname=Column(String(20))
    priv_ip=Column(String(20))
    pub_ip=Column(String(20))
    os_version=Column(String(20))
    start_time=Column(DateTime)

    def __init__(self,vir_id,priv_ip,hostname,pub_ip,os_version,start_time):
        self.vir_id=vir_id
        self.priv_ip=priv_ip
        self.hostname=hostname
        self.pub_ip=pub_ip
        self.os_version=os_version
        self.start_time=start_time

    def __repr__(self):
        return "<Hostinfo('%s','%s','%s','%s','%s')>"%(self.vir_id,self.priv_ip,self.pub_ip,self.hostname,self.os_version)

def main():
    pass

if __name__=="__main__":
    main()

