#!/usr/bin/perl
use strict;
use Log::Log4perl;
use Config::Tiny;

our ($project,$sectionName,$buildHomePath,$buildName);

sub readConf(){
        our $conf = Config::Tiny->read("/srv/salt/deploy_workflow/ini/$project\_getPkgs.ini") || die "$project\_getPkgs.ini, ERROR:$!\n";

        if($sectionName =~ /\Aall\z/){
                our @section_tmp = sort keys %{$conf};
                foreach (@section_tmp){
                        if($_ =~ /common/){
                                next;
                        }else{
                                push (our @section,"$_");
                        }
                }
        }else{
                our @section = split(/,/,$sectionName);
        }

        our $buildName = $conf->{common}->{buildName};
        our $releaseConf = $conf->{common}->{releaseConf};
        our $buildHomePath = $conf->{common}->{buildHomePath};
        our $srcGameSrv =$conf->{common}->{srcGameSrv};
}

sub modifyClientConf(){
        chdir("$buildHomePath/packages/$buildName/client");
        if (-e "shell.html"){
                print "    |__ Modify configuration in shell.xml...\n";
                system("perl -pi -e 's#test_goc#prod_goc#g' ./shell.html");
        }
}

############################## Main program ######################################
our $project = $ARGV[0];
&readConf();
&modifyClientConf();
