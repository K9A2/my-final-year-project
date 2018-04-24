#!/bin/bash
# record the average download speed for 50 times, in Bps
# curl -o /dev/null -s -w %{speed_download} http://47.106.146.168/5M.zip >> ${algorithm}.log
algorithm=cubic

for((i=1;i<=5;i++))
do
    echo round ${i}
    curl -o /dev/null -s -w %{speed_download} http://192.168.1.106/500M.zip >> ${algorithm}.log
    echo "" >> ${algorithm}.log
done
