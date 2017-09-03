# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
import numpy
import re
import matplotlib.pyplot as plt
import pandas as pd


def get_result_dictionary(csv, names):
    data = {}

    for name in names:
        data[name] = []

    for i in range(1, len(csv)):
        # load data for all algorithms
        for j in range(len(csv[i])):
            data[names[j]].append(float(csv[i][j]))

    return data


def read_text_file(file_name):
    target_file = open(file_name)
    lines = target_file.readlines()
    target_file.close()
    for i in range(len(lines)):
        lines[i] = re.sub("[\n|\r|\xef|\xbb|\xbf]", "", lines[i])
        lines[i] = lines[i].split(",")
    return lines


def main():
    """
    Main Function, nothing to comment
    """

    file_path = "./LabRecord/result/curl/"
    file_names = ["curl_lan.csv", "curl_di.csv", "curl_ii.csv"]

    colors = ["orange", "orange", "orange", "orange", "orange", "orange", "orange",
              "orange", "orange", "orange", "orange", "orange"]

    # colors = ["#70AD47", "#4472C4", "#FFC000", "#ED7D31", "#7030A0", "#002060",
    #          "#92D050", "#FF0000", "#C00000", "#833C0B", "#BF9000", "#A8D08D"]
    algorithms = ["cubic", "westwood", "bbr", "scalable", "bic", "highspeed", "htcp", "hybla", "illinois", "vegas",
                  "yeah", "reno"]

    names = ["CUBIC", "Westwood", "BBR", "Scalable", "BIC", "High Speed", "H-TCP", "Hybla", "Illinois", "Vegas",
             "YeAH", "Reno"]

    scenario = file_names[0]
    fsize = 52
    label_size = 35

    # load records
    result = {}
    for file_name in file_names:
        result[file_name] = get_result_dictionary(read_text_file(file_path + file_name), names)

    # print variance
    for name in names:
        print ("%10s  %3.5f" % (name, numpy.median(result[scenario][name])))

    df = pd.DataFrame(result[scenario])

    # draw box charts
    # plt.boxplot(x=df.values, labels=df.columns, whis=1.5)

    plt.yticks(fontsize=fsize)
    plt.ylabel("Average DS (MB\s)", fontsize=fsize)

    i = 0
    f = df.boxplot(sym='r*', patch_artist=True)
    for box in f['boxes']:
        # 箱体边框颜色
        box.set(color='black', linewidth=3)
        # 箱体内部填充颜色
        box.set(facecolor=colors[i])
        i += 1
    for whisker in f['whiskers']:
        whisker.set(color='r', linewidth=3)
    for cap in f['caps']:
        cap.set(color='black', linewidth=3)
    for median in f['medians']:
        median.set(color='red', linewidth=3)
    for flier in f['fliers']:
        flier.set(marker='.', color='#000', alpha=0.5)
    plt.xticks(fontsize=fsize, rotation=45)
    plt.show()

    return


#   Function Main
if __name__ == '__main__':
    main()
