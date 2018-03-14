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


def process(path, exp_name, con_name, out_index, out_exp, out_con):
    exp_byte = 0
    con_byte = 0
    for i in range(1, 4):
        json_exp = json.loads("".join(
            re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) +
                                                         exp_name)))))
        json_con = json.loads("".join(
            re.sub("[\n|\t]", "", "".join(read_text_file(path + str(i) +
                                                         con_name)))))

        exp_byte += json_exp["end"]["sum_sent"]["bytes"] / (1024.0 * 1024.0)
        con_byte += json_con["end"]["sum_sent"]["bytes"] / (1024.0 * 1024.0)

    out_exp.append(exp_byte / 3)
    out_con.append(con_byte / 3)
    #     (x1 + x2)^2
    # -----------------
    # 2 * (x1^2 + x2^2)
    out_index.append(
        (exp_byte + con_byte) * (exp_byte + con_byte) / (2 * ((exp_byte *
                                                               exp_byte) +
                                                              (con_byte *
                                                               con_byte))))


def auto_label(ups, downs, labels, figure):
    for i in range(len(ups)):
        height = ups[i].get_height() + downs[i].get_height()
        plt.text(ups[i].get_x() + ups[i].get_width() / 2.0, height + 400,
                 "%1.2f" % labels[i],
                 ha="center",
                 rotation=90,
                 fontsize=35
                 )
        i += 1


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


def main():
    """
    Main Function, nothing to comment
    """
    scenario = "lan"
    fsize = 52
    label_size = 35

    file_name_base = "../lab-record/result/fairness"

    algorithms = ["bbr", "scalable", "bic", "highspeed", "htcp", "hybla",
                  "illinois", "vegas", "yeah"]
    names = ["BBR", "Scalable", "BIC", "High Speed",
             "H-TCP", "Hybla", "Illinois", "Vegas", "YeAH"]

    test_types = ["vs_reno", "vs_cubic", "vs_itself"]

    vs_reno_exp = []
    vs_reno_con = []

    vs_cubic_exp = []
    vs_cubic_con = []

    vs_itself_exp = []
    vs_itself_con = []
    
    index_reno = []
    index_cubic = []
    index_itself = []

    data = []

    for algorithm in algorithms:
        for test in test_types:
            path_base = file_name_base + "/" + scenario + "/" + test + "/" + \
                algorithm + "/"
            if test == "vs_itself":
                exp_name = names[algorithms.index(algorithm)] + "_1"
                con_name = names[algorithms.index(algorithm)] + "_2"
                exp_filename = "/" + algorithm + "_1.log"
                con_filename = "/" + algorithm + "_2.log"
                process(path_base, exp_filename, con_filename,
                        index_itself, vs_itself_exp, vs_itself_con)
            if test == "vs_reno":
                exp_name = names[algorithms.index(algorithm)]
                con_name = "Reno"
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/reno.log"
                process(path_base, exp_filename, con_filename,
                        index_reno, vs_reno_exp, vs_reno_con)
            if test == "vs_cubic":
                con_name = "CUBIC"
                exp_name = names[algorithms.index(algorithm)]
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/cubic.log"
                process(path_base, exp_filename, con_filename,
                        index_cubic, vs_cubic_exp, vs_cubic_con)

    data.extend(vs_reno_exp[:])
    data.extend(vs_reno_con[:])
    data.extend(vs_cubic_exp[:])
    data.extend(vs_cubic_con[:])
    data.extend(vs_itself_exp[:])
    data.extend(vs_itself_con[:])

    size = 9
    x = numpy.arange(size)

    total_width, n = 1.2, 2.5
    width = 1.0 / n
    x = x - (total_width - width) / 2

    for i in range(0, len(x)):
        x[i] += 0.5 * i

    # Exp
    fig = plt.figure()

    exp_reno = plt.bar(x + 0 * width - 1.2,
                       vs_reno_exp,
                       width=width,
                       label='Testee',
                       alpha=0.5,
                       color="red")
    exp_cubic = plt.bar(x + 1 * width - 1.2,
                        vs_cubic_exp,
                        width=width,
                        label='Testee',
                        alpha=0.5,
                        color="blue")
    exp_itself = plt.bar(x + 2 * width - 1.2,
                         vs_itself_exp,
                         width=width,
                         label='Testee',
                         alpha=0.5,
                         color="black")
    # Con
    con_reno = plt.bar(x + 0 * width - 1.2,
                       vs_reno_con,
                       bottom=vs_reno_exp,
                       width=width,
                       label='Reno',
                       alpha=0.5,
                       color="darkorange")
    auto_label(con_reno, exp_reno, index_reno, fig)
    con_cubic = plt.bar(x + 1 * width - 1.2,
                        vs_cubic_con,
                        bottom=vs_cubic_exp,
                        width=width,
                        label='CUBIC',
                        alpha=0.5,
                        color="lawngreen")
    auto_label(con_cubic, exp_cubic, index_cubic, fig)
    con_itself = plt.bar(x + 2 * width - 1.2,
                         vs_itself_con,
                         bottom=vs_itself_exp,
                         width=width,
                         label='Itself',
                         alpha=0.5,
                         color="dodgerblue")
    auto_label(con_itself, exp_itself, index_itself, fig)

    # Index
    plt.xticks(x + 1.5 * width - 1.2, ["BBR", "Scalable", "BIC", "High Speed",
                                       "H-TCP", "Hybla", "Illinois", "Vegas",
                                       "YeAH"],
               fontsize=fsize,
               rotation="45")
    plt.ylabel("Transferred Data(MB)", fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.ylim(0, numpy.max(data) * 1.5)

    ax = plt.subplot(111)
    handles, labels = ax.get_legend_handles_labels()
    handles.reverse()
    labels.reverse()
    plt.legend(flip(handles, 3), flip(labels, 3),
               loc="upper left", ncol=3, fontsize=label_size)

    plt.show()


#   Function Main
if __name__ == '__main__':
    main()
