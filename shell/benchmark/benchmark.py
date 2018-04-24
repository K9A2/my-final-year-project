# coding=utf-8
# filename: benchmark.py

import json
import re

import matplotlib.pyplot as plt
import numpy as np


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


def get_average_mbps(intervals):
    bps = 0
    for i in range(len(intervals)):
        bps += intervals[i]['sum']['bits_per_second']
    bps /= len(intervals)
    return bps / (1000.0 * 1000.0)


def main():
    # Load and parse json object from file with specific
    path = './2.4g/'
    algorithms = ['cubic', 'reno', 'bbr', 'westwood', 'veno']

    result = []

    for a in algorithms:
        doc = re.sub("[\n|\t]", "", "".join(read_text_file(path + 'benchmark_' + a + '.log')))
        json_object = json.loads("".join(doc))
        result.append(get_average_mbps(json_object['intervals']))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(range(len(result)), result)
    ax.set_xticklabels(algorithms)

    plt.show()

# Function Main
if __name__ == '__main__':
    main()
