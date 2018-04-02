# coding=utf-8
# filename: benchmark.py

"""
Calculat parameters for wireless scenario
"""
import json
import re

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from scipy import stats


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
    """Main function
    """

    # Names of evaluated algorithms
    algorithms = ["bbr", "cubic", "reno", "veno", "westwood"]
    names = ["BBR", "CUBIC", "Reno", "Veno", "Westwood"]

    # Path to folder contains log files
    file_path = "../lab-record/result/wireless/one-client/2.4g/tx-20mw/"

    # Round name in one evaluation
    rounds = ["round_0/", "round_1/", "round_2/"]

    # Settings for plotting
    colors = ["black", "red", "peru", "darkorange", "gold", "yellowgreen",
              "deeppink", "darkviolet", "slateblue", "deepskyblue",
              "mediumturquoise", "lime"]
    font_size = 52

    # Load benchmark to calculate base line
    benchmark_path = file_path + "benchmark.log"
    benchmark_json = json.loads("".join(read_text_file(benchmark_path)))
    rtt = []
    throughput = []
    # Fetch raw meterials from log converted JSON object
    for i in range(len(benchmark_json["intervals"])):
        # Convert from us to ms
        rtt.append(benchmark_json["intervals"][i]["streams"][0]["rtt"] / 1000.0)
        # Convert from bit to Mbits
        throughput.append(benchmark_json["intervals"][i]["streams"][0]
                          ["bits_per_second"] / (1024.0 * 1024.0))
    benchmark = {"rtt": np.average(rtt), "throughput": np.average(throughput)}
    # Print average rtt and throughput
    print "benchmark:"
    print "rtt: " + str(benchmark["rtt"])
    print "throughput: " + str(benchmark["throughput"])

    # Create a new result set for each algorithm
    result = {}
    for algorithm in algorithms:
        rtt = []
        throughput = []
        dictionary = {"rtt": rtt, "throughput": throughput}
        result[algorithm] = dictionary

    # Load evaluation data from log files
    for algorithm in algorithms:
        for r in rounds:
            file_name = file_path + r + algorithm + ".log"
            json_object = json.loads("".join(read_text_file(file_name)))
            intervals = json_object["intervals"]
            for i in range(0, len(intervals)):
                # Convert from us to ms
                result[algorithm]["rtt"].append(
                    intervals[i]["streams"][0]["rtt"] / 1000.0)
                # Convert from bit to Mbits
                result[algorithm]["throughput"].append(
                    intervals[i]["streams"][0]["bits_per_second"] /
                    (1024.0 * 1024.0))

    # Calculate averages for this evaluation
    avg_rtt = []
    avg_throughput = []
    # Key value result set for sortting
    kv_rtt = {}
    kv_throughput = {}
    for algorithm in algorithms:
        avg_rtt.append(np.average(result[algorithm]["rtt"]))
        avg_throughput.append(np.average(result[algorithm]["throughput"]))
        kv_rtt[algorithm] = np.average(result[algorithm]["rtt"])
        kv_throughput[algorithm] = np.average(result[algorithm]["throughput"])

    # Pring statistics
    print "sorted rtt:"
    print sorted(kv_rtt.items(), key=lambda item: item[1])

    print "sorted throughput:"
    print sorted(kv_throughput.items(), key=lambda item: item[1])

    print "max rtt: ", np.max(avg_rtt)
    print "min rtt: ", np.min(avg_rtt)
    print "max throughput: ", np.max(avg_throughput)
    print "min throughput: ", np.min(avg_throughput)

    # Plot RTT in fig 1
    fig_rtt = plt.figure("rtt")
    ax = fig_rtt.add_subplot(111)
    ax.set_xscale("log")
    # Calculate and print CDF figure
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
    # Draw benchmark line and other information
    plt.axvline(benchmark["rtt"], linewidth=3, color="black")
    plt.xlabel("RTT(ms)", fontsize=font_size)
    plt.xticks(fontsize=font_size, y=-0.02)
    # plt.set_xsacle("log")
    plt.ylabel("CDF", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(0, 4000)
    # plt.ylim(0, 4000)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.15)

    # Plot Throughput in fig 2
    fig_throughput = plt.figure("throughput")
    # ax = fig_throughput.add_subplot(111)
    # ax.set_xscale("log")
    # Calculate and print CDF figure
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
    # plot benchmark line
    plt.axvline(benchmark["throughput"], linewidth=3, color="black")
    plt.xlabel("Throughput(Mbits/s)", fontsize=font_size)
    plt.xticks(fontsize=font_size, y=-0.02)
    # ax.set_xsacle("log")
    plt.ylabel("CDF", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(0, 3)
    # plt.ylim(0, 0)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.15)

    plt.show()

    return 0


#   Function Main
if __name__ == '__main__':
    main()
