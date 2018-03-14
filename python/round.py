# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
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
    for i in range(0, len(intervals)):
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
                socket_keys[i], numpy.max(rtt), numpy.min(rtt), numpy.average(rtt), numpy.median(rtt), numpy.var(rtt)))

    # Bandwidth
    print "--------------------------------------------------------"
    print "Bandwidth(Mbit/s)"
    for i in range(len(socket_keys)):
        bandwidth = result[socket_keys[i]]["bits_per_second"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(bandwidth), numpy.min(bandwidth), numpy.average(bandwidth),
                numpy.median(bandwidth), numpy.var(bandwidth)))

    # Retransmission Ratio
    print "--------------------------------------------------------"
    print "Retransmission(packet)"
    for i in range(len(socket_keys)):
        retr = result[socket_keys[i]]["retransmits"]
        print (
            "[%-2d]   %-10.2f%-10.2f%-10.2f%-10.2f%-10.2f" % (
                socket_keys[i], numpy.max(retr), numpy.min(retr), numpy.average(retr), numpy.median(retr),
                numpy.var(retr)))

    # BDP
    print "--------------------------------------------------------"
    print "BDP(Kbit)"
    for i in range(len(socket_keys)):
        rtt = result[socket_keys[i]]["rtt"]
        min_rtt = numpy.min(rtt)

        bandwidth = result[socket_keys[i]]["bits_per_second"]
        max_bandwidth = numpy.max(bandwidth)
        print ("[%-2d]   %-10.3f" % (socket_keys[i], min_rtt * max_bandwidth))


def main():
    """
    Main Function, nothing to comment
    """

    algorithms = ["bbr", "scalable", "bic", "cubic", "highspeed", "htcp", "hybla", "illinois", "vegas", "yeah", "reno"]
    file_path = "./LabRecord/result/true_topo/dc1_to_lan/test_1/round_5/"

    #   Load and parse json object from file with specific
    json_object = {}
    for i in range(0, len(algorithms)):
        json_object[algorithms[i]] = json.loads("".join(read_text_file(file_path + algorithms[i] + ".log")))

    # Print result tables
    print "||Algorithm|Max|Min|Average|Median|Var|"
    print "|-|--|---|------|-------|---|--|"

    result = {}

    for i in range(len(algorithms)):
        intervals = json_object[algorithms[i]]["intervals"]
        rtt = []
        snd_cwnd = []
        bits_per_second = []
        retransmits = []
        flow_table = {}
        for j in range(len(intervals)):
            # Convert to ms
            rtt.append(intervals[j]["streams"][0]["rtt"] / 1000.0)
            snd_cwnd.append(intervals[j]["streams"][0]["snd_cwnd"] / 1024.0)
            bits_per_second.append(intervals[j]["streams"][0]["bits_per_second"] / (1024.0 * 1024.0))
            retransmits.append(intervals[j]["streams"][0]["retransmits"])

        flow_table["rtt"] = rtt
        flow_table["bits_per_second"] = bits_per_second
        flow_table["retransmits"] = retransmits
        flow_table["snd_cwnd"] = snd_cwnd
        result[algorithms[i]] = flow_table

    # Print RTT
    for i in range(len(algorithms)):
        line = result[algorithms[i]]["rtt"]
        if i == 0:
            print "|RTT(ms)|%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (algorithms[i], numpy.max(line), numpy.min(line),
                                                             numpy.average(line), numpy.median(line), numpy.var(line))
        else:
            print "||%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (algorithms[i], numpy.max(line), numpy.min(line),
                                                      numpy.average(line), numpy.median(line), numpy.var(line))

    # Print Bandwidth
    for i in range(len(algorithms)):
        line = result[algorithms[i]]["bits_per_second"]
        if i == 0:
            print "|Bandwidth(Mbit/s)|%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (algorithms[i], numpy.max(line), numpy.min(line),
                                                                       numpy.average(line), numpy.median(line),
                                                                       numpy.var(line))
        else:
            print "||%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (algorithms[i], numpy.max(line), numpy.min(line),
                                                      numpy.average(line), numpy.median(line), numpy.var(line))

    # Print Retransmission Packet
    for i in range(len(algorithms)):
        line = result[algorithms[i]]["retransmits"]
        if i == 0:
            print "|Retransmission Packet	|%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (
                algorithms[i], numpy.max(line), numpy.min(line),
                numpy.average(line), numpy.median(line),
                numpy.var(line))
        else:
            print "||%s|%.2f|%.2f|%.2f|%.2f|%.2f|" % (algorithms[i], numpy.max(line), numpy.min(line),
                                                      numpy.average(line), numpy.median(line), numpy.var(line))

    # Print BDP
    for i in range(len(algorithms)):
        rtt = result[algorithms[i]]["rtt"]
        bit = result[algorithms[i]]["bits_per_second"]
        if i == 0:
            print "|BDP(Kbit)|%s|%5.2f|" % (algorithms[i], numpy.max(bit) * numpy.min(rtt))
        else:
            print "||%s|%5.2f|" % (algorithms[i], numpy.max(bit) * numpy.min(rtt))

    return 0


#   Function Main
if __name__ == '__main__':
    main()
