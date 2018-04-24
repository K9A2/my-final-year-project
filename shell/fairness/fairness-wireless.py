# coding=utf-8
# filename: fairness-wireless.py

import json
import re

import matplotlib.pyplot as plt


# read text file
def read_text_file(file_name):
    target_file = open(file_name)
    lines = target_file.readlines()

    target_file.close()
    return lines


def get_average_mbps(intervals, field):
    s = 0
    for i in range(len(intervals)):
        s += intervals[i]['streams'][0][field]
    s /= len(intervals)
    return s


# get the averages for previous n seconds
def get_n_average_array(intervals, field, n, unit):
    result = [0.0]
    averages = float(len(intervals)) / float(n)
    index = 0
    for i in range(int(averages)):
        index += n
        s = 0
        for j in range(index - n, index):
            s += intervals[i]['streams'][0][field]
        result.append(float(s) / float(n * unit))
    return result


def get_sum_array(a, b):
    s = []
    for i in range(len(a)):
        s.append(a[i] + b[i])
    return s


def fetch_result(file_name, n):
    # fetch result
    result = {}
    doc = re.sub("[\n|\t]", "", "".join(
        read_text_file(file_name)))
    json_object = json.loads("".join(doc))
    # get averages for rtt and throughput
    result['avg_mbps'] = get_average_mbps(
        json_object['intervals'], 'bits_per_second') / (1000.0 * 1000.0)
    result['avg_rtt'] = get_average_mbps(
        json_object['intervals'], 'rtt') / 1000.0
    # get array for rtt and throughput
    result['rtt'] = get_n_average_array(json_object['intervals'], 'rtt', n, 1000.0)
    result['mbps'] = get_n_average_array(
        json_object['intervals'], 'bits_per_second', n, (1000.0 * 1000.0))
    return result


def plot_line_chart(x, y, label):
    plt.plot(x, y, label=label)


def get_fairness_index(a, b):
    if a == 0:
        a = 0.000001
    if b == 0:
        b = 0.000001
    new_a = float(a)
    new_b = float(b)
    return (new_a + new_b) * (new_a + new_b) / (2 * (new_a * new_a + new_b * new_b))


def main():

    # path_base = ['./2.4g/', './5g']
    path_base = './5g/'
    # t = ['vs_cubic', 'vs_itself']
    t = 'vs_itself'

    # algorithms = ['cubic', 'reno', 'bbr', 'westwood', 'veno']
    a = 'veno'

    n = 30
    line_width = 6
    font_size = 36

    exp_file_name = path_base + t + '/' + a + '.log'
    con_file_name = path_base + t + '/' + a + '_' + t + '.log'

    exp = fetch_result(exp_file_name, n)
    con = fetch_result(con_file_name, n)

    print 'exp group:'
    print 'exp average rtt: ' + str(exp['avg_rtt'])
    print 'exp average mbps: ' + str(exp['avg_mbps'])

    print 'con group:'
    print 'con average rtt: ' + str(con['avg_rtt'])
    print 'con average mbps: ' + str(con['avg_mbps'])

    index = []
    fairness_index = []
    for i in range((900 / n) + 1):
        index.append(i * n)
        fairness_index.append(get_fairness_index(exp['mbps'][i], con['mbps'][i]))

    plt.figure('fig_rtt')
    plt.grid(linestyle="--", linewidth=2)
    plt.plot(index, exp['rtt'], label='Host A', linewidth=line_width)
    plt.plot(index, con['rtt'], label='Host B', linewidth=line_width)
    plt.xticks(fontsize=font_size, y=-0.02)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Time(s)", fontsize=font_size)
    plt.ylabel("RTT(ms)", fontsize=font_size)

    plt.legend(fontsize=font_size)
    plt.subplots_adjust(left=0.08, right=0.93, top=0.96, bottom=0.11)

    sum_mbps = []
    for i in range(len(exp['mbps'])):
        sum_mbps.append(exp['mbps'][i] + con['mbps'][i])

    fig_mbps = plt.figure('fig_mbps')
    ax2 = fig_mbps.add_subplot(111)
    plt.grid(linestyle="--", linewidth=2)
    plt_mbps_exp, = plt.plot(index, exp['mbps'], label='Host A', linewidth=line_width)
    plt_mbps_con, = plt.plot(index, con['mbps'], label='Host B', linewidth=line_width)
    plt_mbps_sum, = plt.plot(index, sum_mbps, label='Sum of Host A and Host B', linewidth=line_width)
    plt.xticks(fontsize=font_size, y=-0.02)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Time(s)", fontsize=font_size)
    plt.ylabel("Throughput(Mbps)", fontsize=font_size)

    ax3 = ax2.twinx()
    plt_mbps_index, = ax3.plot(index, fairness_index, label='Jain`s Fairness INdex', linewidth=line_width,
                               color='orange')
    plt.yticks(fontsize=font_size)
    plt.ylabel("Jain`s Fairness Index", fontsize=font_size)
    plt.ylim(0.5, 1.0)

    plt.legend(handles=[plt_mbps_exp, plt_mbps_con, plt_mbps_sum, plt_mbps_index],
               bbox_to_anchor=(0., 1.02, 1., .102),
               loc=3, ncol=2, mode="expand", borderaxespad=0., fontsize=font_size)

    plt.subplots_adjust(left=0.08, right=0.93, top=0.83, bottom=0.11)

    plt.show()


# Function Main
if __name__ == '__main__':
    main()
