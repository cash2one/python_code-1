#! /bin/bash
now=`date '+%Y_%m_%d_%H_%M_%S'`
cp /srv/$1/logs/catalina.out /srv/$1/logs/catalina.out.$now
echo "">/srv/$1/logs/catalina.out
