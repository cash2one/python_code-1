#!/usr/bin/perl

####################################################
#   Modified by Wayne on Aug 3 2015
#   Purpose: Get packages from test env.
#   Change Logs:
#   Aug 3 2015
#       Update the cmdstat for fail
#   Aug 4 2015
#       Add the log output and ERROR check for getFiles and bk2S3
#       Add sub function log_check
#       dos2unix test
####################################################

use strict;
use Config::Tiny;

our (%hash,@section,@moduleVer);
our ($conf,$project,$sectionName,$buildName,$releaseConf,$buildHomePath,$srcGameSrv,$moduleVer);
our $success = "\033[32;1;5msuccess\033[m";
our $fail = "\033[31;1;5mfail\033[m";

###############################################################################
sub readConf(){
	print "Now section is $project $sectionName and start reading config file...\n";
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
	our @moduleVer = split(/,/,$moduleVer);

	foreach(@section){
		if ($conf->{$_} eq ""){
			print "Section name doesn't exist, please check $_ find correct section!\n";
			exit(1);
		}
	}
}
  
sub getFiles(){
	print "    |__ Create build folder\n";
	system("mkdir -p $buildHomePath/packages/$buildName") unless (-e "$buildHomePath/packages/$buildName");
	chdir("$buildHomePath/packages/$buildName");
	print "    |__ Clean all files in build folder\n";
	system("rm -fr $buildHomePath/packages/$buildName/*");
	print "    |__ $success...\n";

	foreach my $section (@section){
		our $uploadPkgs = $conf->{$section}->{uploadPkgs};
		our @uploadPkgs=split(/,/,$uploadPkgs);
		our $rsyncTagPath = $conf->{$section}->{rsyncTagPath};
	
		foreach(@uploadPkgs){
			print "    |__ Start to get package $_ ...\n";
			print "    |__ The cmd is:\n";
			print "    |__ rsync -vzrtopg --delete --progress qa\@$srcGameSrv\:\:$rsyncTagPath/$_/ ./$_\n";
			`rsync -vzrtopg --delete --progress qa\@$srcGameSrv\:\:$rsyncTagPath/$_/ ./$_ > /tmp/getPkgs.log 2>&1`;
			print "    |__ Finished to get package $_ ...\n";
			&log_check();
		}
	}
}

sub get_version{
	@hash{@section}=@moduleVer;
	our $num_moduleVer=scalar(@moduleVer);
	foreach my $section (@section){
		our $uploadPkgs = $conf->{$section}->{uploadPkgs};
		our @uploadPkgs=split(/,/,$uploadPkgs);
		if ($num_moduleVer == 1){
		        foreach(@uploadPkgs){
				system("echo $moduleVer > $buildHomePath/packages/$buildName/$_/version");
				&cmdstat();
				print "    |__ get now big version $project $_ $moduleVer... [Finished]\n";
		        }
		}else{
		        foreach(@uploadPkgs){
				system("echo $hash{$section} > $buildHomePath/packages/$buildName/$_/version");
				&cmdstat();
				print "    |__ get now big version $project $_ $hash{$section}... [Finished]\n";
		        }
		}
	}
}

sub createPkgs(){
	chdir("$buildHomePath/packages/$buildName");
	
	opendir PH,"./";
	foreach (readdir PH){
	        chomp $_;
		if ( $_ !~ /^\.|tar.gz$/ ){
			print "    |__ Start creating $_...\n";
			system("tar -zcf $_.tar.gz ./$_");
			&cmdstat();
			print "    |__ $success...\n";
	        }
	}
	closedir (PH);

	print "Backup packages to $buildHomePath/bak/$buildName folder...\n";
	system("mkdir -p $buildHomePath/bak/$buildName") unless(-e "$buildHomePath/bak/$buildName");
	my $time=`date +%Y%m%d-%H`;
	chomp($time);
	my @tar = glob "$buildHomePath/packages/$buildName/*.tar.gz";
	foreach(@tar){
		$_ = ~/$buildHomePath\/packages\/$buildName\/(.*)\.tar\.gz/;
		my $file=$1;
		print "    |__ Start copy $file...\n";
		system("cp -f $buildHomePath/packages/$buildName/$file.tar.gz $buildHomePath/bak/$buildName/$file-$time.tar.gz");
		&cmdstat();
		print "    |__ $success...\n";
	}
}

sub modifyConf(){
	foreach(@section){
		our $uploadPkgs = $conf->{$_}->{uploadPkgs};
		our @uploadPkgs=split(/,/,$uploadPkgs);
		foreach(@uploadPkgs){
			print "    |__ Start modify $_ configuration\n";
			print "    |__ The cmd is:\n";
			print "    |__ /usr/bin/perl $buildHomePath/deploy_workflow/common/modifyConfig.py $releaseConf $_";
			`/usr/bin/perl $buildHomePath/deploy_workflow/common/modifyConfig.py $releaseConf $_`;
			print "    |__ Stop modify $_ configuration\n";
		}
	}
}

sub delExpireBak(){
	foreach(@section){
		system("/usr/bin/perl /srv/salt/deploy_workflow/common/delExpireBak.pl $project $_");
		&cmdstat();
	}
}

sub bk2S3(){
	`s3cmd sync $buildHomePath/bak/$buildName/ s3://aspectgaming-databackup/pkg/$buildName/ > /tmp/getPkgs.log 2>&1`;
	&log_check();
}

#cmdstatus check
sub cmdstat(){
	if($? != 0 ){
		print "    |__ $fail\n";
		exit
	}
}

#log check
sub log_check(){
	`> /tmp/getPkgs.log`;
        my $result=`cat /tmp/getPkgs.log`;
        if($result =~ /error:/i){
                my $flag=`grep -i "error" /tmp/getPkgs.log`;
                print "    |__ [ERROR] $flag";
                print "    |__ $fail\n";
                exit;
        }else{
                print "    |__ $success...\n";
        }
}

############################## Main program ######################################
if (scalar(@ARGV)<2){
	print "Usage: getPkgs.pl [project name] [section name in project file] [version]\n e.g. getPkgs.pl goc all v1.1.1\n";
	exit(1);
}

print "*** Start getPkgs.pl\n";
our $project = $ARGV[0];
our $sectionName = $ARGV[1];
our $moduleVer = $ARGV[2];
&readConf();

print "Get packages from servers\n";
my $startTime = time();
&getFiles();
my $totalTime = time()-$startTime;
print "    |__ It takes $totalTime secs to get packages\n";
    
print "Modify configuration\n";
&modifyConf();
if($project =~ /goc/){
	print "    |__ Start modify client configuration\n";
	print "    |__ The cmd is:\n";
	print "    |__ /usr/bin/perl /srv/salt/deploy_workflow/goc/modifyClientConf.pl $project\n";
	`/usr/bin/perl /srv/salt/deploy_workflow/goc/modifyClientConf.pl $project`;
	&cmdstat();
	print "    |__ Stop modify client configuration\n";
}

print "Get server version\n";
&get_version();

print "Build tar packages...\n";
&createPkgs();

print "Delete back file\n";
&delExpireBak();

print "Backup packages to S3 on AWS\n";
&bk2S3();
print "*** Finished getPkgs.pl $success\n";