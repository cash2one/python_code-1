#!/bin/bash

OPENVPN_PID=`ps -ef | grep "openvpn" | grep -Ev "grep|\.sh" | awk '{print $2}'`
if [ -n "$OPENVPN_PID"  ]; then
    echo "Warn: OPENVPN is still running!"
     exit 1
fi

/etc/init.d/openvpn start
