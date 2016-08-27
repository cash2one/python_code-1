#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
# This is a Web Server for UserManager

import tornado.httpserver                         # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import orm                                        # 引入刚刚编写的orm层代码

define( 'port', default = 9998, help = 'run on the given port', type = int )

host_orm = orm.HostManagerORM()

class MainHandler( tornado.web.RequestHandler ):
        '''
            MainHandler shows all data and a form to add new user
        '''
        def get( self ):
                # show all data and a form
                title = 'Host Manager V0.2'

                hosts = host_orm.GetAllHost()
                self.render( 'templates/HostManager.html', title = title, hosts = hosts )

        def post( self ):
                pass

class AddHostHandler( tornado.web.RequestHandler ):
        '''
            AddUserHandler collects info to create new user
        '''
        def get( self ):
                pass

        def post( self ):
                # Collect info and create a user record in the database
                host_info = {
                                'host_name':self.get_argument( 'host_name' ),
                                'private_ip':self.get_argument( 'private_ip' ),
                                'public_ip':self.get_argument( 'public_ip' ),
                                'os':self.get_argument( 'os' ),
                                'mem':self.get_argument( 'mem' )
                                }
                host_orm.CreateNewHost( host_info )
                url='http://localhost:%s'%options.port
                self.redirect( url )

class EditHostHandler( tornado.web.RequestHandler ):
        '''
            Show a page to edit user info,
            user name is given by GET method
        '''
        def get( self ):
                host_info = host_orm.GetHostByName( self.get_argument( 'host_name' ) )
                self.render( 'templates/EditHostInfo.html', host_info = host_info )

        def post( self ):
                pass

class UpdateHostInfoHandler( tornado.web.RequestHandler ):
        '''
            Update user info by given list
        '''
        def get( self ):
                pass

        def post( self ):
                host_orm.UpdateHostInfoByName({
                        'host_name':self.get_argument( 'host_name' ),
                        'private_ip':self.get_argument( 'private_ip' ),
                        'public_ip':self.get_argument( 'public_ip' ),
                        'os':self.get_argument( 'os' ),
                        'mem':self.get_argument( 'mem' ),
                        })
                url='http://localhost:%s'%options.port
                self.redirect( url )

class DeleteHostHandler( tornado.web.RequestHandler ):
        '''
            Delete user by given name
        '''
        def get( self ):

                host_orm.DeleteHostByName( self.get_argument( 'host_name' ) )

                url='http://localhost:%s'%options.port
                self.redirect( url )

        def post( self ):
                pass
class GetDataHostHandler(tornado.web.RequestHandler):
        def get(self):
                check_hostname=self.get_argument('host_name')
                hostinfo=getHostinfoByName(check_hostname)
                host_orm.UpdateHostInfoByName(hostinfo)
                
                url='http://localhost:%s'%options.port
                self.redirect( url )
        def post(self):
                pass


def getHostinfoByName(hostname):
        import ansible.runner
        files_ini = '/home/qa/miles/script/ansible/vm.ini'
        runner = ansible.runner.Runner(host_list=files_ini, module_name='setup' \
                                       , pattern=hostname)
        output = runner.run()
        
        hostinfo = dict()
        hostinfo['host_name']=hostname
        hostinfo['mem'] = output['contacted'][hostname]['ansible_facts']['ansible_memory_mb']['real']['total']
        hostinfo['os'] = "%s %s" % (output['contacted'][hostname]['ansible_facts']['ansible_distribution'] \
                                                   , output['contacted'][hostname]['ansible_facts'][
                                                   'ansible_distribution_version'])
        ips = output['contacted'][hostname]['ansible_facts']['ansible_all_ipv4_addresses']
        priv_ip_l = []
        pub_ip_l = []
        for ip in ips.split(','):
                if str(ip.split('.')[0]) in ['172', '192', '10']:
                        priv_ip_l.append(ip)
                else:
                        pub_ip_l.append(ip)
        hostinfo['private_ip'] = priv_ip_l
        hostinfo['public_ip'] = pub_ip_l
        
        return hostinfo

def MainProcess():
        tornado.options.parse_command_line()
        application = tornado.web.Application( [
                ( r'/', MainHandler ),
                ( r'/AddHost', AddHostHandler ),
                ( r'/EditHost', EditHostHandler ),
                ( r'/GetDataHost', GetDataHostHandler ),
                ( r'/DeleteHost', DeleteHostHandler ),
                ( r'/UpdateHostInfo', UpdateHostInfoHandler ),
        ])

        http_server = tornado.httpserver.HTTPServer( application )
        http_server.listen( options.port )
        tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
        MainProcess()
