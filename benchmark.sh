#   Start the benchmark to test the network.

server=202.120.38.44

iperf3 -c ${server} -J | tee benchmark.log
