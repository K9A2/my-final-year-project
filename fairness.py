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


def get_result_dictionary(intervals):
    """
    Get results in a dictionary accessed by different socket keys.

    :param intervals:   Test intervals in list
    :param keys:        Socket keys in list

    :return:            Result in dictionary
    """
    result = {}

    #   Create entries in dictionary for all flows
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
    result[0] = flow_table

    # Load data for each flow
    for i in range(len(intervals)):
        for j in range(len(intervals[i]['streams'])):
            #   Convert rtt from us to ms
            result[0]["rtt"].append(intervals[i]['streams'][j]['rtt'] / 1000.0)
            #   Convert from bit to Kbits
            result[0]["snd_cwnd"].append(float(
                intervals[i]['streams'][j]['snd_cwnd'] / 1024.0))
            #   Convert from bit to Mbit
            result[0]["bits_per_second"].append(
                intervals[i]['streams'][j]['bits_per_second'] / (1024 * 1024))
            result[0]["retransmits"].append(
                intervals[i]['streams'][j]['retransmits'])

    return result


def get_socket_keys(intervals):
    """
    Get socket IDs for keys used in result dictionary.

    :param intervals:   Intervals form JSON Object in list

    :return:            Socket IDs in list
    """
    socket_keys = []

    for i in range(len(intervals[0]["streams"])):
        socket_keys.append(intervals[0]["streams"][i]["socket"])

    return socket_keys


def draw_charts(result, labels, socket_keys):
    """
    Draw line charts for rtt, snd_cwnd, bits_per_second and retransmits.

    """
    colors = ["#fd6126", "#029ED9", "#81FF38", "#FF7438", "#FF4238", "#A3159A"]
    size = 1
    styles = ["o", "."]

    #   Get the lengthe of Y stick
    y = []
    for i in range(len(result[socket_keys[0]]['rtt'])):
        y.append(i)

    # get jain`s fairness index
    band_0 = result[socket_keys[0]]['bits_per_second']
    band_1 = result[socket_keys[1]]['bits_per_second']
    index = []
    for i in range(len(band_0)):
        x0 = band_0[i]
        x1 = band_1[i]
        if x0 == 0:
            x0 = 0.1
        if x1 == 0:
            x1 = 0.1
        index.append(((x0 + x1) * (x0 + x1)) / (2 * ((x0 * x0) + (x1 * x1))))

    # bandwidth
    band_fig = plt.figure("bandwidth")
    plt.ylabel("Bandwidth(Mbits/sec)")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['bits_per_second'],
                 colors[i], label=labels[i], linewidth=size)
    plt.legend()
    band_fig.savefig("bandwidth.pdf", format="pdf")
    band_fig.show()

    # retransmit
    retr_fig = plt.figure("retransmit")
    plt.ylabel("Packets number")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['retransmits'],
                 colors[i], label=labels[i], linewidth=size)
    plt.legend()
    retr_fig.savefig("retr.pdf", format="pdf")
    retr_fig.show()

    # congestion window size
    cong_fig = plt.figure("cong")
    plt.ylabel("Size(KB)")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['snd_cwnd'],
                 colors[i], label=labels[i], linewidth=size)
    plt.legend()
    cong_fig.savefig("cong.pdf", format="pdf")
    cong_fig.show()

    # rtt
    rtt_fig = plt.figure("rtt")
    plt.ylabel("ms")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['rtt'],
                 colors[i], label=labels[i], linewidth=size)
    plt.legend()
    rtt_fig.savefig("rtt.pdf", format="pdf")
    rtt_fig.show()

    # fairness index
    rtt_fig = plt.figure("index")
    plt.plot(y, index, colors[i], label="Fariness Index", linewidth=size)
    plt.legend()
    rtt_fig.savefig("index.pdf", format="pdf")
    rtt_fig.show()

    plt.show()


def get_statistics(result, socket_keys):
    """
    Print statistics for given result.

    :param result:      Result in dict
    :param socket_keys: Socket IDs in list
    """

    '''
    Get min, max, median and variance for RTT, bandwidth, Retransmission
    Ratio and BDP for all streams
    '''

    # Print table header
    print "ID     Max       Min       Median    Average   Variances"

    # RTT
    print "--------------------------------------------------------"
    print "RTT(ms)"
    for i in range(len(socket_keys)):
        rtt = result[socket_keys[i]]["rtt"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(rtt), numpy.min(rtt), numpy.median(rtt), numpy.average(rtt), numpy.var(rtt)))

    # Bandwidth
    print "--------------------------------------------------------"
    print "Bandwidth(Mbit/s)"
    for i in range(len(socket_keys)):
        bandwidth = result[socket_keys[i]]["bits_per_second"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(bandwidth), numpy.min(bandwidth), numpy.median(bandwidth),
                numpy.average(bandwidth), numpy.var(bandwidth)))

    # Retransmission Ratio
    print "--------------------------------------------------------"
    print "Retransmission(packet)"
    for i in range(len(socket_keys)):
        retr = result[socket_keys[i]]["retransmits"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(retr), numpy.min(retr), numpy.median(retr), numpy.average(retr),
                numpy.var(retr)))

    # BDP
    print "--------------------------------------------------------"
    print "BDP(Mbit)"
    for i in range(len(socket_keys)):
        rtt = result[socket_keys[i]]["rtt"]
        bandwidth = result[socket_keys[i]]["bits_per_second"]

        bdp = []
        for j in range(len(rtt)):
            bdp.append(rtt[j] * bandwidth[j])

        print ("[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
        socket_keys[i], numpy.max(bdp), numpy.min(bdp), numpy.median(bdp), numpy.average(bdp), numpy.var(bdp)))


def parse_arguments():
    """
    Parse arguments from command line input. Empty now.
    """
    print "Hello world"


def print_usage():
    """
    Print usage when user input wrong arguments. Empty now.
    """
    print "Hello world"


def main():
    """
    Main Function, nothing to comment
    """
    #   Load and parse json object from file with specific
    labels = ["Hybla", "Reno"]
    experimented = "./LabRecord/result/fairness/international/vs_reno/hybla/3/hybla.log"
    contrasted = "./LabRecord/result/fairness/international/vs_reno/hybla/3/reno.log"

    doc_experimented = re.sub("[\n|\t]", "", "".join(read_text_file(experimented)))
    doc_contrasted = re.sub("[\n|\t]", "", "".join(read_text_file(contrasted)))

    json_experimented = json.loads("".join(doc_experimented))
    json_contrasted = json.loads("".join(doc_contrasted))

    #   Important JSON objects
    intervals_exp = json_experimented["intervals"]
    intervals_con = json_contrasted["intervals"]

    #   Socket IDs to get data from result dictionary
    result_exp = get_result_dictionary(intervals_exp)
    result_con = get_result_dictionary(intervals_con)

    result = {0: result_exp[0], 1: result_con[0]}

    draw_charts(result, labels, socket_keys=[0, 1])

    return 0


#   Function Main
if __name__ == '__main__':
    main()
