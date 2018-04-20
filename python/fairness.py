# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
import re
import matplotlib.pyplot as plt
import numpy
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


def process(path, exp_name, con_name, out_index):
    exp_byte = 0
    con_byte = 0
    for i in range(1, 4):
        json_exp = json.loads("".join(
            re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) +
                                                         exp_name)))))
        json_con = json.loads("".join(
            re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) +
                                                         con_name)))))
        for j in range(len(json_exp['intervals'])):
            exp_byte += json_exp["intervals"][j]["streams"][0]["bits_per_second"] / (1000.0 * 1000.0 * 8)
        for j in range(len(json_con['intervals'])):
            con_byte += json_con["intervals"][i]["streams"][0]["bits_per_second"] / (1000.0 * 1000.0 * 8)

    #     (x1 + x2)^2
    # -----------------
    # 2 * (x1^2 + x2^2)
    out_index.append(
        (exp_byte + con_byte) * (exp_byte + con_byte) / (2 * ((exp_byte *
                                                               exp_byte) +
                                                              (con_byte *
                                                               con_byte))))


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


def main():
    """
    Main Function, nothing to comment
    """

    file_name_base = "./lab-record/result/fairness/"
    scenarios = ['lan', 'wan1', 'wan2']
    scenario = scenarios[2]

    algorithms = ["bbr", "scalable", "bic", "highspeed", "htcp", "hybla",
                  "illinois", "vegas", "yeah"]
    names = ["BBR", "Scalable", "BIC", "High Speed",
             "H-TCP", "Hybla", "Illinois", "Vegas", "YeAH"]

    test_types = ["vs_reno", "vs_cubic", "vs_itself"]

    fsize = 36
    
    index_reno = []
    index_cubic = []
    index_itself = []

    data = []
    
    print 'Loadint statistics for ' + file_name_base + '/' + scenario

    for algorithm in algorithms:
        for test in test_types:
            path_base = file_name_base + "/" + scenario + "/" + test + "/" + \
                algorithm + "/"
            if test == "vs_itself":
                exp_name = names[algorithms.index(algorithm)] + "_1"
                con_name = names[algorithms.index(algorithm)] + "_2"
                print path_base + exp_name
                print path_base + con_name
                exp_filename = "/" + algorithm + "_1.log"
                con_filename = "/" + algorithm + "_2.log"
                process(path_base, exp_filename, con_filename, index_itself)
            if test == "vs_reno":
                exp_name = names[algorithms.index(algorithm)]
                con_name = "Reno"
                print path_base + exp_name
                print path_base + con_name
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/reno.log"
                process(path_base, exp_filename, con_filename, index_reno)
            if test == "vs_cubic":
                con_name = "CUBIC"
                exp_name = names[algorithms.index(algorithm)]
                print path_base + exp_name
                print path_base + con_name
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/cubic.log"
                process(path_base, exp_filename, con_filename, index_cubic)

    size = 9
    x = numpy.arange(size)

    total_width, n = 1.2, 2.5
    width = 1.0 / n
    x = x - (total_width - width) / 2

    for i in range(0, len(x)):
        x[i] += 0.5 * i

    # Exp
    fig = plt.figure()

    # Con
    con_reno = plt.bar(x + 0 * width - 1.2,
                       index_reno,
                       width=width,
                       label='Against Reno',
                       alpha=0.5,
                       color="darkorange")

    con_cubic = plt.bar(x + 1 * width - 1.2,
                        index_cubic,
                        width=width,
                        label='Against CUBIC',
                        alpha=0.5,
                        color="lawngreen")

    con_itself = plt.bar(x + 2 * width - 1.2,
                         index_itself,
                         width=width,
                         label='Against Another Same CCA',
                         alpha=0.5,
                         color="dodgerblue")

    # Index
    plt.xticks(x + 1.5 * width - 1.2, ["BBR", "Scalable", "BIC", "High Speed",
                                       "H-TCP", "Hybla", "Illinois", "Vegas",
                                       "YeAH"],
               fontsize=fsize,
               rotation="45")
    plt.ylabel("Jain`s Fairness Index", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.ylim(0.5, 1.1)

    ax = plt.subplot(111)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
              ncol=3, mode="expand", borderaxespad=0., fontsize=fsize)

    plt.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.2)

    plt.show()


#   Function Main
if __name__ == '__main__':
    main()
