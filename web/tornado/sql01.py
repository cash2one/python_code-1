#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

from sqlalchemy import Column,String,create_engine,Integer,DateTime
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
import pdb

Base=declarative_base()

engine = create_engine('mysql://root:aspect@172.18.188.147/aspect',convert_unicode=True,echo=False,encoding='utf8')
DBSession=sessionmaker(bind=engine)

class Serverlist(Base):
    __tablename__='serverlist'
    #Column('id',Integer,primary_key=True)
    id=Column(Integer,primary_key=True,autoincrement =True)
    vir_id=Column(String(20))
    priv_ip=Column(String(20))
    info=relationship("Serverinfo")


class Serverinfo(Base):
    __tablename__="serverinfo"
    id=Column(Integer,primary_key=True,autoincrement =True)
    vir_id=Column(String(20))
    hostname=Column(String(20))
    priv_ip=Column(String(20))
    pub_ip=Column(String(20))
    os_version=Column(String(20))
    start_time=Column(DateTime)
   # list=relationships("Serverlist",back_populates="info")


def get_virtual_id():
    import uuid
    return str(uuid.uuid4())



def add_server():
    session=DBSession()
    new_server=Serverinfo(hostname='test-02',priv_ip='192.168.10.11',pub_ip="114.24.1.23",os_version="ubun-14",start_time="2016-05-14 08:09:10")
    session.add(new_server)
    session.commit()
    session.close()

def get_serverlist():
    session=DBSession()
    server=session.query(Serverlist).filter(Serverlist.id==1).one()
    #server=session.query(Serverlist).filter(Serverlist.info.any(Serverinfo.id==1)).first()
    print "type :",type(server)
    print "hostname :",server.info
    session.close()


if __name__=="__main__":
    #add_server()
    get_serverlist()

