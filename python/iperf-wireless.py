# coding=utf-8
# filename: benchmark.py

"""
计算无线场景中的各项 TCP 性能参数
"""
import json
import re

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from pylab import *
from scipy import stats


def read_text_file(file_name):
    target_file = open(file_name)
    lines = target_file.readlines()

    target_file.close()
    return lines


def get_result_dictionary(intervals, keys):
    result = {}

    #   Create entries in dictionary for all flows
    for i in range(len(keys)):
        flow_table = {}
        rtt_list = []
        snd_cwnd_list = []
        bits_per_second_list = []
        retransmits_list = []
        flow_table["rtt"] = rtt_list
        flow_table["snd_cwnd"] = snd_cwnd_list
        flow_table["bits_per_second"] = bits_per_second_list
        flow_table["retransmits"] = retransmits_list
        #   Add entry
        result[keys[i]] = flow_table

    # Load data for each flow
    for i in range(0, len(intervals)):
        for j in range(len(intervals[i]['streams'])):
            ID = intervals[i]['streams'][j]['socket']
            #   Convert rtt from us to ms
            result[ID]["rtt"].append(
                intervals[i]['streams'][j]['rtt'] / 1000.0)
            #   Convert from bit to Kbits
            result[ID]["snd_cwnd"].append(
                intervals[i]['streams'][j]['snd_cwnd'] / 1024)
            #   Convert from bit to Mbit
            result[ID]["bits_per_second"].append(
                intervals[i]['streams'][j]['bits_per_second'] / (1024 * 1024))
            result[ID]["retransmits"].append(
                intervals[i]['streams'][j]['retransmits'])

    return result


def sort_by_value(d):
    items = d.items()
    back_items = [[v[1], v[0]] for v in items]
    back_items.sort()
    return [back_items[i][1] for i in range(0, len(back_items))]


def main():

    algorithms = ["bbr", "cubic", "reno", "veno", "westwood"]
    names = ["bbr", "cubic", "reno", "veno", "westwood"]
    file_path = "../lab-record/result/wireless/one-client/"
    round_name = ["round_0/", "round_1/", "round_2/"]

    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "s"]
    colors = ["black", "red", "peru", "darkorange", "gold", "yellowgreen",
              "deeppink", "darkviolet", "slateblue", "deepskyblue",
              "mediumturquoise", "lime"]

    fsize = 52

    result = {}

    for algorithm in algorithms:
        rtt = []
        bw = []
        dictionary = {"rtt": rtt, "bw": bw}
        result[algorithm] = dictionary

    # load benchmark
    benchmark_path = file_path + "benchmark.log"
    benchmark_json = json.loads("".join(read_text_file(benchmark_path)))
    rtt = []
    bw = []
    for i in range(len(benchmark_json["intervals"])):
        rtt.append(benchmark_json["intervals"][i]["streams"][0]["rtt"] / 1000)
        bw.append(benchmark_json["intervals"][i]["streams"]
                  [0]["bits_per_second"] / (1024 * 1024))

    benchmark = {"rtt": np.average(rtt), "bw": np.average(bw)}

    print "rtt: " + str(benchmark["rtt"])
    print "bw: " + str(benchmark["bw"])

    # data
    for algorithm in algorithms:
        for r in round_name:
            file_name = file_path + r + algorithm + ".log"
            json_object = json.loads("".join(read_text_file(file_name)))
            intervals = json_object["intervals"]
            for i in range(0, len(intervals)):
                result[algorithm]["rtt"].append(
                    intervals[i]["streams"][0]["rtt"] / 1000.0)
                result[algorithm]["bw"].append(
                    intervals[i]["streams"][0]["bits_per_second"] /
                    (1024.0 * 1024.0))

    # print average throughput
    avg_rtt = []
    avg_bw = []
    kv_rtt = {}
    kv_bw = {}
    for algorithm in algorithms:
        print algorithm
        avg_rtt.append(np.average(result[algorithm]["rtt"]))
        avg_bw.append(np.average(result[algorithm]["bw"]))
        kv_rtt[algorithm] = np.average(result[algorithm]["rtt"])
        kv_bw[algorithm] = np.average(result[algorithm]["bw"])

    print "sorted rtt"
    print sorted(kv_rtt.items(), key=lambda item: item[1])

    print "sorted bw"
    print sorted(kv_bw.items(), key=lambda item: item[1])

    print "max rtt"
    print np.max(avg_rtt)
    print "min rtt"
    print np.min(avg_rtt)
    print "max bw"
    print np.max(avg_bw)
    print "min bw"
    print np.min(avg_bw)

    # print average rtt

    # plot rtt in fig 1
    fig_rtt = plt.figure("rtt")
    for i in range(len(algorithms)):
        sorted_data = np.sort(result[algorithms[i]]["rtt"])

        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)

        plt.plot(sorted_data, yvals, linewidth=4,
                 label=names[i], color=colors[i])
    # plot benchmark line
    plt.axvline(benchmark["rtt"], linewidth=3, color="black")
    plt.xlabel("RTT(ms)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    plt.xlim(0, 4000)
    plt.ylabel("Cumulative Distribution", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    # plot bandwidth in fig 2
    fig_bw = plt.figure("bandwidth")
    for i in range(len(algorithms)):
        sorted_data = np.sort(result[algorithms[i]]["bw"])

        yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)

        plt.plot(sorted_data, yvals, linewidth=4,
                 label=names[i], color=colors[i])
    # plot benchmark line
    plt.axvline(benchmark["bw"], linewidth=3, color="black")
    plt.xlabel("Throughput(Mbits/s)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    # plt.xlim(0, 3)
    plt.ylabel("Cumulative Distribution", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.legend(fontsize=35, numpoints=100, loc='lower right')

    plt.show()

    return 0


#   Function Main
if __name__ == '__main__':
    main()
