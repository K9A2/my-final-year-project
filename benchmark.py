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


def get_result_dictionary(intervals, keys):
    """
    Get results in a dictionary accessed by different socket keys.

    :param intervals:   Test intervals in list
    :param keys:        Socket keys in list

    :return:            Result in dictionary
    """
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
    for i in range(len(intervals)):
        for j in range(len(intervals[i]['streams'])):
            ID = intervals[i]['streams'][j]['socket']
            #   Convert rtt from us to ms
            result[ID]["rtt"].append(intervals[i]['streams'][j]['rtt'] / 1000.0)
            #   Convert from bit to Kbits
            result[ID]["snd_cwnd"].append(
                intervals[i]['streams'][j]['snd_cwnd'] / 1024)
            #   Convert from bit to Mbit
            result[ID]["bits_per_second"].append(
                intervals[i]['streams'][j]['bits_per_second'] / (1024 * 1024))
            result[ID]["retransmits"].append(
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


def draw_charts(result, socket_keys):
    """
    Draw line charts for rtt, snd_cwnd, bits_per_second and retransmits.

    :param  result:         Result in dict
    :param  socket_keys:    Socket IDs in list
    """
    colors = ["#fd6126", "#029ED9", "#81FF38", "#FF7438", "#FF4238", "#A3159A"]
    size = 2.0
    #   Get the lengthe of Y stick
    y = []
    for i in range(len(result[socket_keys[0]]['rtt'])):
        y.append(i)

    # Draw N lines in the same chart
    plt.subplot(2, 2, 1)
    plt.title("Bits per second")
    plt.ylabel("Bandwidth(Mbits/sec)")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['bits_per_second'],
                 colors[i], label=socket_keys[i], linewidth=size)

    plt.subplot(2, 2, 2)
    plt.title("Retransmitted packet number")
    plt.ylabel("Packets number")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['retransmits'],
                 colors[i], label=socket_keys[i], linewidth=size)

    plt.subplot(2, 2, 3)
    plt.title("Congestion window size")
    plt.ylabel("Size(KB)")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['snd_cwnd'],
                 colors[i], label=socket_keys[i], linewidth=size)

    plt.subplot(2, 2, 4)
    plt.title("RTT")
    plt.ylabel("ms")
    for i in range(len(socket_keys)):
        plt.plot(y, result[socket_keys[i]]['rtt'],
                 colors[i], label=socket_keys[i], linewidth=size)

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
                socket_keys[i], numpy.max(bandwidth), numpy.min(bandwidth), numpy.median(bandwidth), numpy.average(bandwidth), numpy.var(bandwidth)))

    # Retransmission Ratio
    print "--------------------------------------------------------"
    print "Retransmission(packet)"
    for i in range(len(socket_keys)):
        retr = result[socket_keys[i]]["retransmits"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(retr), numpy.min(retr), numpy.median(retr), numpy.average(retr), numpy.var(retr)))

    # BDP
    print "--------------------------------------------------------"
    print "BDP(Mbit)"
    for i in range(len(socket_keys)):
        rtt = result[socket_keys[i]]["rtt"]
        bandwidth = result[socket_keys[i]]["bits_per_second"]

        bdp = []
        for j in range(len(rtt)):
            bdp.append(rtt[j] * bandwidth[j])

        print ("[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (socket_keys[i], numpy.max(bdp), numpy.min(bdp), numpy.median(bdp), numpy.average(bdp), numpy.var(bdp)))


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
    file_name = "./LabRecord/result/true_topo/aliyun1_to_amazon/test_0/round_0/bbr.log"
    doc = re.sub("[\n|\t]", "", "".join(read_text_file(file_name)))
    json_object = json.loads("".join(doc))

    #   Important JSON objects
    intervals = json_object["intervals"]
    start = json_object["start"]
    end = json_object["end"]

    #   Socket IDs to get data from result dictionary
    socket_keys = get_socket_keys(intervals)

    result = get_result_dictionary(intervals, socket_keys)

    get_statistics(result, socket_keys)

    draw_charts(result, socket_keys)

    return 0


#   Function Main
if __name__ == '__main__':
    main()
