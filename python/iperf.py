# coding=utf-8
# filename: benchmark.py

"""
Calculat parameters for wired scenario
"""
import json

import matplotlib.pyplot as plt
import numpy as np


def read_text_file(file_name):
    """Read log file contains JSON string

    Args:
        file_name (string): [File path to log file]

    Returns:
        [list]: [Lines in log file]
    """
    target_file = open(file_name)
    lines = target_file.readlines()

    target_file.close()
    return lines


def main():
    """
    Main Function, nothing to comment
    """

    # Names of evaluated algorithms
    algorithms = ["bbr", "scalable", "bic", "cubic", "highspeed", "htcp",
                  "hybla", "illinois", "vegas", "yeah", "reno"]
    names = ["BBR", "Scalable", "BIC", "CUBIC", "High Speed", "H-TCP", "Hybla",
             "Illinois", "Vegas", "YeAH", "Reno"]

    # Path to evaluation log folder
    file_path = "../lab-record/result/true_topo/"

    tests = ["test_0/", "test_1/"]
    round_name = ["round_0/", "round_1/", "round_2/", "round_3/", "round_4/",
                  "round_5/"]

    # Settings from plotting
    colors = ["black", "red", "peru", "darkorange", "gold", "yellowgreen",
              "deeppink", "darkviolet", "slateblue", "deepskyblue",
              "mediumturquoise", "lime"]
    font_size = 52

    # Scanerios to be plotted
    scenarios = ["dc1_to_lan/", "dc2_to_aliyun2/", "aliyun1_to_amazon/"]
    scenario = scenarios[1]

    # Load benchmark
    benchmark_path = file_path + scenario + "benchmark/benchmark.log"
    benchmark_json = json.loads("".join(read_text_file(benchmark_path)))
    rtt = []
    throughput = []
    for i in range(len(benchmark_json["intervals"])):
        rtt.append(benchmark_json["intervals"][i]["streams"][0]["rtt"] / 1000)
        throughput.append(benchmark_json["intervals"][i]["streams"]
                          [0]["bits_per_second"] / (1024 * 1024))
    # Print bechmark results
    benchmark = {"rtt": np.average(rtt), "throughput": np.average(throughput)}
    print "rtt: " + str(benchmark["rtt"])
    print "throughput: " + str(benchmark["throughput"])

    # Create result set for test result
    result = {}
    for algorithm in algorithms:
        rtt = []
        throughput = []
        dictionary = {"rtt": rtt, "throughput": throughput}
        result[algorithm] = dictionary

    # Load date into result set
    for t in tests:
        for algorithm in algorithms:
            for r in round_name:
                file_name = file_path + scenario + t + r + algorithm + ".log"
                json_object = json.loads("".join(read_text_file(file_name)))
                intervals = json_object["intervals"]
                for i in range(0, len(intervals)):
                    # Convert us into ms
                    result[algorithm]["rtt"].append(
                        intervals[i]["streams"][0]["rtt"] / 1000.0)
                    # Convert bits to Mbits
                    result[algorithm]["throughput"].append(
                        intervals[i]["streams"][0]["bits_per_second"] /
                        (1024.0 * 1024.0))

    # Calculate statistics
    avg_rtt = []
    avg_throughput = []
    # Result dictionary for sortting
    kv_rtt = {}
    kv_throughput = {}
    for algorithm in algorithms:
        print algorithm
        avg_rtt.append(np.average(result[algorithm]["rtt"]))
        avg_throughput.append(np.average(result[algorithm]["throughput"]))
        kv_rtt[algorithm] = np.average(result[algorithm]["rtt"])
        kv_throughput[algorithm] = np.average(result[algorithm]["throughput"])

    # Print statistics
    print "sorted rtt:"
    print sorted(kv_rtt.items(), key=lambda item: item[1])
    print "sorted throughput: "
    print sorted(kv_throughput.items(), key=lambda item: item[1])

    print "max rtt: ", np.max(avg_rtt)
    print "min rtt: ", np.min(avg_rtt)
    print "max throughput: ", np.max(avg_throughput)
    print "min throughput: ", np.min(avg_throughput)

    # Draw rtt CDF
    fig_rtt = plt.figure("rtt")
    for i in range(len(algorithms)):
        sorted_data = np.sort(result[algorithms[i]]["rtt"])
        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
        plt.plot(
            sorted_data,
            yvals,
            linewidth=4,
            label=names[i],
            color=colors[i]
        )
    # Draw benchmark line
    plt.axvline(benchmark["rtt"], linewidth=3, color="black")
    # Xticks and Yticks
    plt.xlabel("RTT(ms)", fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.ylabel("CDF", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(220, 350)
    # plt.ylim(0, 0)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    # Draw throughput CDF
    fig_throughput = plt.figure("bandwidth")
    for i in range(len(algorithms)):
        sorted_data = np.sort(result[algorithms[i]]["throughput"])
        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
        plt.plot(
            sorted_data,
            yvals,
            linewidth=4,
            label=names[i],
            color=colors[i]
        )
    # Draw benchmark line
    plt.axvline(benchmark["throughput"], linewidth=3, color="black")
    # Xticks and Yticks
    plt.xlabel("Throughput(Mbits/s)", fontsize=font_size)
    plt.xticks(fontsize=font_size)
    plt.ylabel("Cumulative Distribution", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(0, 3)
    # plt.ylim(0, 0)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    plt.show()

    return 0


#   Function Main
if __name__ == '__main__':
    main()
