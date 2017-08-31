# coding=utf-8
# filename: benchmark.py

"""
This file includes the procedure to process the data from iperf3 with single
thread, i.e. "iperf3 -c hostname [-i time]" and draws a LINE CHART for it.
"""
import json
import numpy
import matplotlib.pyplot as plt


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
    file_path = "./LabRecord/result/true_topo/dc1_to_lan/"
    round_name = ["round_0", "round_1", "round_2", "round_3", "round_4", "round_5"]
    benchmark_name = "benchmark/benchmark.log"

    colors = ["#70AD47", "#4472C4", "#FFC000", "#ED7D31", "#7030A0", "#002060",
              "#92D050", "#FF0000", "#C00000", "#833C0B", "#BF9000", "#A8D08D"]

    # load benchmark result
    benchmark = {}
    benchmark_file = json.loads("".join(read_text_file(file_path + benchmark_name)))

    intervals = benchmark_file["intervals"]
    rtt = []
    bandwidth = []
    retransmits = []
    for i in range(0, len(intervals)):
        # convert rtt from us to ms
        rtt.append(intervals[i]["streams"][0]["rtt"] / 1000)
        bandwidth.append(intervals[i]["streams"][0]["bits_per_second"] / (1024 * 1024))
        retransmits.append(intervals[i]["streams"][0]["retransmits"])

    benchmark["rtt"] = rtt
    benchmark["bandwidth"] = bandwidth
    benchmark["retransmits"] = retransmits

    # set their median as base line
    bandwidth_base = numpy.average(benchmark["bandwidth"])
    rtt_base = numpy.average(benchmark["rtt"])
    retransmits_base = numpy.average(benchmark["retransmits"])

    # load data structure for result
    result = {}
    for i in range(0, len(algorithms)):
        algorithm = {}
        rtt = []
        retransmits = []
        bandwidth = []
        efficiency = []
        algorithm["rtt"] = rtt
        algorithm["bandwidth"] = bandwidth
        algorithm["retransmits"] = retransmits
        algorithm["efficiency"] = efficiency
        result[algorithms[i]] = algorithm

    # load test results for all algorithms, ith algorithm
    for i in range(len(algorithms)):
        # jth round for ith algorithm
        for j in range(len(round_name)):
            round_result = json.loads("".join(read_text_file(file_path + "test_1/" + round_name[j] + "/" + algorithms[i] + ".log")))
            intervals = round_result["intervals"]
            # load result data for this round
            rtt = []
            efficiency = []
            bandwidth = []
            retransmits = []
            for k in range(len(intervals)):
                rtt.append(intervals[k]["streams"][0]["rtt"] / 1000.0)
                bandwidth.append(intervals[k]["streams"][0]["bits_per_second"] / (1024.0 * 1024.0))
                retransmits.append(intervals[k]["streams"][0]["retransmits"])
                efficiency.append(intervals[k]["streams"][0]["bits_per_second"] / (1024.0 * 1024.0) / bandwidth_base)
            result[algorithms[i]]["rtt"].append(numpy.average(rtt))
            result[algorithms[i]]["efficiency"].append(numpy.average(efficiency))
            result[algorithms[i]]["bandwidth"].append(numpy.average(bandwidth))
            result[algorithms[i]]["retransmits"].append(numpy.average(retransmits))

    x = []
    for i in range(0, 6):
        x.append(i)

    # rtt
    rtt_1 = plt.figure("rtt_1")
    plt.subplot(111)
    plt.title("RTT(ms)")
    plt.ylabel("time(ms)")
    for i in range(0, 6):
        plt.plot(x, result[algorithms[i]]["rtt"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(rtt_base, color="black", linewidth=4)
    plt.legend()
    rtt_1.show()

    rtt_2 = plt.figure("rtt_2")
    plt.subplot(111)
    plt.title("RTT(ms)")
    plt.ylabel("time(ms)")
    for i in range(6, len(algorithms)):
        plt.plot(x, result[algorithms[i]]["rtt"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(rtt_base, color="black", linewidth=4)
    plt.legend()
    rtt_2.show()

    # bandwidth
    bandwidth_1 = plt.figure("bandwidth_1")
    plt.subplot(111)
    plt.title("bandwidth(Mbit/s)")
    plt.ylabel("bandwidth(Mbit/s)")
    for i in range(0, 6):
        plt.plot(x, result[algorithms[i]]["bandwidth"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(bandwidth_base, color="black", linewidth=4)
    plt.legend()
    bandwidth_1.show()

    bandwidth_1 = plt.figure("bandwidth_2")
    plt.subplot(111)
    plt.title("bandwidth(Mbit/s)")
    plt.ylabel("bandwidth(Mbit/s)")
    for i in range(6, len(algorithms)):
        plt.plot(x, result[algorithms[i]]["bandwidth"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(bandwidth_base, color="black", linewidth=4)
    plt.legend()
    bandwidth_1.show()

    # efficiency
    efficiency_1 = plt.figure("efficiency_1")
    plt.subplot(111)
    plt.title("percent")
    plt.ylabel("percent")
    for i in range(0, 6):
        plt.plot(x, result[algorithms[i]]["efficiency"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(1, color="black", linewidth=4)
    plt.legend()
    efficiency_1.show()

    efficiency_1 = plt.figure("efficiency_2")
    plt.subplot(111)
    plt.title("percent")
    plt.ylabel("percent")
    for i in range(6, len(algorithms)):
        plt.plot(x, result[algorithms[i]]["efficiency"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(1, color="black", linewidth=4)
    plt.legend()
    efficiency_1.show()

    # retransmits
    retransmits_1 = plt.figure("retransmits_1")
    plt.subplot(111)
    plt.title("packet")
    plt.ylabel("packet")
    for i in range(0, 6):
        plt.plot(x, result[algorithms[i]]["retransmits"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(retransmits_base, color="black", linewidth=4)
    plt.legend()
    retransmits_1.show()

    retransmits_1 = plt.figure("retransmits_2")
    plt.subplot(111)
    plt.title("packet)")
    plt.ylabel("packet")
    for i in range(6, len(algorithms)):
        plt.plot(x, result[algorithms[i]]["retransmits"], colors[i], label=algorithms[i], linewidth=4)
    plt.axhline(retransmits_base, color="black", linewidth=4)
    plt.legend()
    retransmits_1.show()

    plt.show()

    return 0


#   Function Main
if __name__ == '__main__':
    main()
