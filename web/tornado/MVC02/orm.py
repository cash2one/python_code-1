#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
from sqlalchemy import *
from sqlalchemy.orm import *

# Settings to connect to mysql database
database_setting = { 'database_type':'mysql',
                'connector':'mysqlconnector',
                'user_name':'root',
                'password':'aspect',
                'host_name':'172.18.188.147',
                'database_name':'HostManager',
                }


class Host( object ):
        def __init__( self, host_name, private_ip,
                        public_ip, os, mem ):
                self.host_name = host_name
                self.private_ip = private_ip
                self.public_ip = public_ip
                self.os = os
                self.mem = mem


class HostManagerORM():
        def __init__( self ):

                self.engine = create_engine(
                                database_setting[ 'database_type' ] +
                                '+' +
                                database_setting[ 'connector' ] +
                                '://' +
                                database_setting[ 'user_name' ] +
                                ':' +
                                database_setting[ 'password' ] +
                                '@' +
                                database_setting[ 'host_name' ] +
                                '/' +
                                database_setting[ 'database_name' ]
                                )
                self.metadata = MetaData( self.engine )
                self.host_table = Table( 'host', self.metadata,
                                autoload = True )


                mapper( Host, self.host_table )


                self.Session = sessionmaker()
                self.Session.configure( bind = self.engine )

                self.session = self.Session()

        def CreateNewHost( self, host_info ):
                new_host = Host(
                                host_info[ 'host_name' ],
                                host_info[ 'private_ip' ],
                                host_info[ 'public_ip' ],
                                host_info[ 'os' ],
                                host_info[ 'mem' ]
                                )
                self.session.add( new_host )
                self.session.commit()

        def GetHostByName( self, host_name ):
                return self.session.query( Host ).filter_by(
                                host_name = host_name ).all()[ 0 ]

        def GetAllHost( self ):
                return self.session.query( Host )

        def UpdateHostInfoByName( self, host_info ):
                host_name = host_info[ 'host_name' ]
                host_info_without_name = { 'private_ip':host_info[ 'private_ip' ],
                                'public_ip':host_info[ 'public_ip' ],
                                'os':host_info[ 'os' ],
                                'mem':host_info[ 'mem' ]
                                }
                self.session.query( Host ).filter_by( host_name = host_name ).update(
                                host_info_without_name )
                self.session.commit()

        def DeleteHostByName( self, host_name ):                  # 删除指定用户名的用户
                host_need_to_delete = self.session.query( Host ).filter_by(
                                host_name = host_name ).all()[ 0 ]
                self.session.delete( host_need_to_delete )
                self.session.commit()
