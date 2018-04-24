# coding=utf-8
# filename: benchmark.py

"""
Calculate parameters for wired scenario
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
    markers=[".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "s"]

    # Scanerios to be plotted
    scenarios = ["lan_to_dc1/", "aliyun2_to_dc2/", "amazon_to_aliyun1/"]
    scenario = scenarios[2]

    # Load benchmark
    benchmark_path = file_path + scenario + "benchmark/benchmark.log"
    benchmark_json = json.loads("".join(read_text_file(benchmark_path)))
    rtt = []
    throughput = []
    retransmits = []
    for i in range(len(benchmark_json["intervals"])):
        rtt.append(benchmark_json["intervals"][i]["streams"][0]["rtt"] / 1000.0)
        throughput.append(benchmark_json["intervals"][i]["streams"]
                          [0]["bits_per_second"] / (1024.0 * 1024.0))
        retransmits.append(benchmark_json["intervals"][i]["streams"][0]["retransmits"])

    benchmark = {
        "rtt": np.average(rtt),
        "throughput": np.average(throughput),
        "retransmits": np.average(retransmits)
    }
    # Print average rtt and throughput
    print "benchmark:"
    print "rtt: " + str(benchmark["rtt"])
    print "throughput: " + str(benchmark["throughput"])
    print "retransmits: " + str(benchmark["retransmits"])

    # Create result set for test result
    result = {}
    for algorithm in algorithms:
        rtt = []
        throughput = []
        retransmits = []
        dictionary = {
            "rtt": rtt,
            "throughput": throughput,
            "retransmits": retransmits
        }
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
                    # Add retransmits results
                    result[algorithm]["retransmits"].append(
                        intervals[i]["streams"][0]["retransmits"]
                    )

    # Calculate averages for this evaluation
    avg_rtt = []
    avg_throughput = []
    avg_retransmits = []
    # Key value result set for sortting
    kv_rtt = {}
    kv_throughput = {}
    kv_retransmits = {}
    for algorithm in algorithms:
        avg_rtt.append(np.average(result[algorithm]["rtt"]))
        avg_throughput.append(np.average(result[algorithm]["throughput"]))
        avg_retransmits.append(np.average(result[algorithm]["retransmits"]))
        kv_rtt[algorithm] = np.average(result[algorithm]["rtt"])
        kv_throughput[algorithm] = np.average(result[algorithm]["throughput"])
        kv_retransmits[algorithm] = np.average(result[algorithm]["retransmits"])

    # Pring statistics
    print "sorted rtt:"
    print sorted(kv_rtt.items(), key=lambda item: item[1])

    print "sorted throughput:"
    print sorted(kv_throughput.items(), key=lambda item: item[1])

    print "sorted retransmits:"
    print sorted(kv_retransmits.items(), key=lambda item: item[1])

    print "max rtt: ", np.max(avg_rtt)
    print "min rtt: ", np.min(avg_rtt)
    print "max throughput: ", np.max(avg_throughput)
    print "min throughput: ", np.min(avg_throughput)
    print "max retransmits: ", np.max(avg_retransmits)
    print "min retransmits: ", np.min(avg_retransmits)

    # Plot RTT in fig 1
    fig_rtt = plt.figure("rtt")
    ax = fig_rtt.add_subplot(111)
    ax.set_xscale("log")
    # Calculate and print CDF figure
    plt.grid(linestyle="--", linewidth=2)
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
    # plot benchmark line
    plt.axvline(benchmark["rtt"], linewidth=3, color="black")
    plt.xlabel("RTT(ms)", fontsize=font_size)
    plt.xticks(fontsize=font_size, y=-0.02)
    # ax.set_xsacle("log")
    plt.ylabel("CDF", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(0, 3)
    # plt.ylim(0, 0)
    plt.legend(fontsize=35, loc='lower right')

    plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.15)

    # Plot Throughput in fig 2
    fig_throughput = plt.figure("throughput")
    # ax = fig_throughput.add_subplot(111)
    # ax.set_xscale("log")
    # Calculate and print CDF figure
    plt.grid(linestyle = "--", linewidth=2)
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
    plt.xlabel("Throughput(Mbps)", fontsize=font_size)
    plt.xticks(fontsize=font_size, y=-0.02)
    # ax.set_xsacle("log")
    plt.ylabel("CDF", fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # plt.xlim(0, 3)
    # plt.ylim(0, 0)
    plt.legend(fontsize=35, loc='lower right')

    plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.15)

    # Plot Retransmits in fig 3
    fig_retr = plt.figure("retransmits")
    # ax = fig_throughput.add_subplot(111)
    # ax.set_xscale("log")
    # Calculate and print CDF figure
    plt.grid(linestyle="--", linewidth=2)
    for i in range(len(algorithms)):
        sorted_data = np.sort(result[algorithms[i]]["retransmits"])
        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
        plt.plot(
            sorted_data,
            yvals,
            linewidth=4,
            label=names[i],
            color=colors[i]
        )
    # plot benchmark line
    plt.axvline(benchmark["retransmits"], linewidth=3, color="black")
    plt.xlabel("Retransmits(packet/s)", fontsize=font_size)
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
