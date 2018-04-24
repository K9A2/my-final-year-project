#!/bin/bash

algorithms=("cubic" "reno" "bbr" "westwood" "veno")

# algorithms=("bbr" "scalable" "bic" "cubic" "highspeed" "htcp" "hybla" "illinois" "vegas" "yeah" "reno")

second=900

# Switch algorithms and run the test
for algorithm in ${algorithms[*]}
do
    echo $algorithm > /proc/sys/net/ipv4/tcp_congestion_control
    ls_date=`date  +'%Y_%m_%d_%T'`
    echo ${ls_date}: ${algorithm} 15min 20mw
    iwconfig wlp2s0 1> settings_${algorithm}.log
    iperf3 -c 192.168.1.100 -t ${second} -J 1> ${algorithm}.log
done

mkdir 5g
mkdir 5g/vs_cubic
mv *.log 5g/vs_cubic
