#!/bin/bash
#   Filename:       run.sh
#   Version:        1.0
#   Date:           2017-08-11 19:46
#   Author:         stormlin
#   Email:          lin-jinting@outlook.com
#   Website:        www.stormlin.com
#   Descripton:     Automatically switchs tcp congestion control algorithm, and 
#                   runs iperf3 network test. Finally, records the results in 
#                   log files with timestamp and algorithm name attached on file 
#                   name.
#   Copyright:      2017 - stormlin
#   License:        MIT

#------------------------------- Code Starts -----------------------------------

algorithms=("bbr" "scalable" "bic" "cubic" "highspeed" "htcp" "hybla" "illinois" "vegas" "yeah" "reno")

second=600
rounds=6

# Switch algorithms and run the test
for((i=0;i<${rounds};i++))
do
    mkdir round_${i}
    for algorithm in ${algorithms[*]}
    do
        echo "-----------------------------------------------------"
        echo $algorithm > /proc/sys/net/ipv4/tcp_congestion_control 
        ls_date=`date  +'%Y_%m_%d_%T'`
        echo ${ls_date}
        echo round_${i}_${algorithm}
        iperf3 -c 125.218.213.22 -t ${second} -V -J | tee ./round_${i}/iperf3_${ls_date}_${algorithm}_r${i}_l${second}_i1_s0_json.log
        sleep 3
    done
done
