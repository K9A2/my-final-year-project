#!/bin/bash
# Start the benchmark to test the network.

# iperf3 -c ${server} -t 3600 -V -J | tee benchmark.log

server=192.168.1.100

algorithms=("cubic" "reno" "bbr" "veno" "westwood")
tests=4

second=3600

for algorithm in ${algorithms[*]}
do
    echo ${algorithm} > /proc/sys/net/ipv4/tcp_congestion_control
    ls_date=`date  +'%Y_%m_%d_%T'`
    echo ${ls_date}: ${algorithm}
    # dump settings
    iwconfig wlp2s0 1> iwconfig_${algorithm}.log
    # run the test and output its result to a log file
    iperf3 -c ${server} -t ${second} -J 1> benchmark_${algorithm}.log
done
