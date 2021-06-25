#!/bin/bash


check_counts=5
current_status_1=`/usr/sbin/ss -tlpn|grep 808|grep haproxy|wc -l`
if [ $current_status_1 -ne $check_counts ];then
        sleep 1
        current_status_2=`/usr/sbin/ss -tlpn|grep 808|grep haproxy|wc -l`
        if [ $current_status_2 -ne $check_counts ];then
                echo `date +'%Y-%m-%d %H:%M:%S'` ' restart haproxy.....' >> /xxx/logs/check_ha.log
                systemctl restart haproxy
                sleep 2
                current_status_3=`/usr/sbin/ss -tlpn|grep 808|grep haproxy|wc -l`
                if [ $current_status_3 -ne $check_counts ];then
                        sleep 2
                        current_status_4=`/usr/sbin/ss -tlpn|grep 808|grep haproxy|wc -l`
                        if [ $current_status_4 -ne $check_counts ];then
                                /opt/SecureSphere/etc/impctl/bin/impctl  gateway stop
                                echo `date +'%Y-%m-%d %H:%M:%S'` ' stop impave.....' >> /xxx/logs/check_ha.log
                        fi
                fi
        fi
fi
