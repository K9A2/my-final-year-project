#   Start the benchmark to test the network.

server=10.42.0.1

iperf3 -c ${server} -t 3600 -V -J | tee benchmark.log
