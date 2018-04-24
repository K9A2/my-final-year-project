# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import re
import statsmodels.api as sm
import matplotlib.patches as mpatches
import pandas as pd
from scipy import stats

import itertools


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


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


def main():
    """
    Main Function, nothing to comment
    """

    algorithms = ["bbr", "scalable", "bic", "cubic", "highspeed", "htcp",
                  "hybla", "illinois", "vegas", "yeah", "reno"]
    names = ["BBR", "Scalable", "BIC", "CUBIC", "High Speed", "H-TCP", "Hybla",
             "Illinois", "Vegas", "YeAH", "Reno"]
    file_path = "../lab-record/result/true_topo/"
    # round_name = ["round_0/", "round_1/", "round_2/", "round_3/", "round_4/",
    # "round_5/"]
    round_name = ["round_0/"]

    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "s"]
    colors = ["black", "red", "peru", "darkorange", "gold", "yellowgreen",
              "deeppink", "darkviolet", "slateblue", "deepskyblue",
              "mediumturquoise", "lime"]

    scenarios = ["lan_to_dc1/", "aliyun2_to_dc2/", "amazon_to_aliyun1/"]

    # tests = ["test_0/", "test_1/"]
    tests = ["test_0/"]

    scenario = scenarios[2]

    fsize = 52

    result = {}
    avg = {}
    for algorithm in algorithms:
        result[algorithm] = []
        avg[algorithm] = []

    # data
    for t in tests:
        for algorithm in algorithms:
            for r in round_name:
                file_name = file_path + scenario + t + r + algorithm + ".log"
                json_object = json.loads("".join(read_text_file(file_name)))
                intervals = json_object["intervals"]
                for i in range(0, len(intervals)):
                    result[algorithm].append(
                        intervals[i]["streams"][0]["bits_per_second"] /
                        (1024.0 * 1024.0))

    for algorithm in algorithms:
        for i in range(1, 21):
            temp = []
            for j in range(0, 30):
                temp.append(result[algorithm][i - j])
            avg[algorithm].append(np.average(temp))

    # plot bandwidth in fig 2
    time = []
    for i in range(0, 20):
        time.append((i + 1) * 30)

    for i in range(len(algorithms)):
        plt.plot(time, avg[algorithms[i]], linewidth=3,
                 label=names[i], color=colors[i], marker=markers[i])

    plt.xlabel("Time(s)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    # plt.xlim(0, 3)
    plt.ylabel("Throughput(Mbps)", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    # plt.ylim(1.05, 1.2)

    ax = plt.subplot(111)
    handles, labels = ax.get_legend_handles_labels()
    # plt.legend(fontsize=35, loc='upper center')
    plt.legend(flip(handles, 3), flip(labels, 3),
               loc="upper center", ncol=4, fontsize=35)

    plt.show()

    return 0


#   Function Main
if __name__ == '__main__':
    main()
