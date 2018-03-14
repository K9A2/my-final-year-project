# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
import re
import matplotlib.pyplot as plt
import numpy as np
import itertools


def read_text_file(file_name):
    """
    Read experiment result in text file

    :param file_name:   File path to result file
    :return:    Data text in list, line by line
    """
    target_file = open(file_name)
    lines = target_file.readlines()

    target_file.close()
    return lines


def process(path, exp_name, con_name, out_index, out_exp, out_con):
    exp_byte = 0
    con_byte = 0
    for i in range(1, 4):
        json_exp = json.loads("".join(re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) + exp_name)))))
        json_con = json.loads("".join(re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) + con_name)))))

        exp_byte += json_exp["end"]["sum_sent"]["bytes"] / (1024.0 * 1024.0)
        con_byte += json_con["end"]["sum_sent"]["bytes"] / (1024.0 * 1024.0)

    out_exp.append(exp_byte / 3)
    out_con.append(con_byte / 3)
    #     (x1 + x2)^2
    # -----------------
    # 2 * (x1^2 + x2^2)
    out_index.append(
        (exp_byte + con_byte) * (exp_byte + con_byte) / (2 * ((exp_byte * exp_byte) + (con_byte * con_byte))))


def auto_label(downs, labels):
    for i in range(len(downs)):
        height = downs[i].get_height()
        plt.text(downs[i].get_x() + downs[i].get_width() / 2.0, height + 400, "%1.2f" % labels[i],
                 ha="center",
                 rotation=90,
                 fontsize=35)
        i += 1


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


def main():
    """
    Main Function, nothing to comment
    """

    fsize = 52
    label_size = 35

    file_name_base = "./LabRecord/result/true_topo/"

    algorithms = ["bbr", "cubic", "hybla", "illinois", "vegas", "reno"]
    names = ["BBR", "CUBIC", "Hybla", "Illinois", "Vegas", "Reno"]

    test_types = ["vs_reno", "vs_cubic", "vs_itself"]

    round_name = ["round_0/", "round_1/", "round_2/", "round_3/", "round_4/", "round_5/"]

    scenarios = ["dc2_to_aliyun2/", "aliyun1_to_amazon/"]
    scenario_names = ["di", "ii"]

    tests = ["test_0/", "test_1/"]

    MBytes = 1024.0
    duration = 600

    di = []
    ii = []

    # Raw data
    data = {}
    for n in scenario_names:
        data[n] = {}
        for algo in algorithms:
            data[n][algo] = []
    for i in range(len(scenario_names)):
        for algo in algorithms:
            for test in tests:
                for r in round_name:
                    bytes = []
                    file_name = file_name_base + scenarios[i] + test + r + algo + ".log"
                    json_object = json.loads("".join(re.sub("[\n|\t]", "", "".join(read_text_file(file_name)))))
                    for k in range(len(json_object["intervals"])):
                        bytes.append(json_object["intervals"][k]["sum"]["bits_per_second"] / 1024.0 / 1024.0)
                    data[scenario_names[i]][algo].append(np.average(bytes))

    # Calculate result from raw data
    values = []
    for algo in algorithms:
        di.append(np.average(data["di"][algo]))
        values.append(np.average(data["di"][algo]))
    for algo in algorithms:
        ii.append(np.average(data["ii"][algo]))
        values.append(np.average(data["ii"][algo]))

    # Chart
    fig = plt.figure()
    size = 6
    x = np.arange(size)

    total_width, n = 1.2, 2.5
    width = 1.0 / n
    x = x - (total_width - width) / 2

    bar_di = plt.bar(x + 0 * width - 1.2, di,
                       width=width,
                       label='Domestic Internet',
                       alpha=0.5,
                       color="red")
    auto_label(bar_di, di)

    bar_ii = plt.bar(x + 1 * width - 1.2, ii,
                        width=width,
                        label='International Internet',
                        alpha=0.5,
                        color="blue")
    auto_label(bar_ii, ii)

    # Labels
    plt.xticks(x + 1.5 * width - 1.2, ["BBR", "Scalable", "BIC", "High Speed", "H-TCP", "Hybla", "Illinois",
                                       "Vegas", "YeAH"], fontsize=fsize, rotation="45")
    plt.ylabel("Average Throughput(Mbps)", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.ylim(0, np.max(values) * 1.2)

    # legend
    ax = plt.subplot(111)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(flip(handles, 3), flip(labels, 3), loc="upper center", ncol=3, fontsize=label_size)

    plt.show()


#   Function Main
if __name__ == '__main__':
    main()
