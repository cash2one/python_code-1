#!/usr/bin/perl

use strict;
use Log::Log4perl;
use Config::Tiny;

open DATE,"date +%Y-%m-%d-%H|" or die "can'n pipe from date:$!";
our $time_date=<DATE>;
chomp $time_date;

our $num_expire=3;
our $project = $ARGV[0];
our $sectionName = $ARGV[1];
our ($buildName,$buildHomePath);
our (@list_module_pkg,@date_uniq_module,@date_name_module,@date_uniq_module,@list_module_pkg,@date_uniq_module);
our ($lenth_date_uniq,%hash);

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
	our $buildHomePath = $conf->{common}->{buildHomePath};
}

sub delExpireBak(){
	chdir("$buildHomePath/bak/$buildName");
        our @name_pkgs = glob("*");
        foreach my $name_pkg (@name_pkgs){
		chomp($name_pkg);
		if($name_pkg =~ $sectionName){
			push(our @list_module_pkg,"$name_pkg");

		}
	}
	foreach our $name_module_pkg (@list_module_pkg){
		my @list_module_pkg=split(/\./,$name_module_pkg);
		my @list_name_module=split(/-/,@list_module_pkg[0]);
		push (our @date_name_module,"@list_name_module[1]");
	}
	@date_uniq_module=grep { ++$hash{$_} < 2 } @date_name_module;
	$lenth_date_uniq=scalar(@date_uniq_module);
	if ($lenth_date_uniq > $num_expire){
		for (my $i=0; $i < $lenth_date_uniq-$num_expire; $i++){
			foreach (@list_module_pkg){
				if($_ =~ /@date_uniq_module[$i]/){
					print "   |__ Start delete $_...\n";
					system("rm -rf $_");
#					system("ls $_");
				}
			}
		}	
	}else{
		print "    |__ There is no package to delete\n";
	}
}

############################## Main program ######################################
if (scalar(@ARGV)<2){
        print "Usage: delExpireBak.pl [project name] [module name in project file] \n e.g. delExpireBak.pl goc gameserver\n";
        exit(1);
}

&readConf();
&delExpireBak();
