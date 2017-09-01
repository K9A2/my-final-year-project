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


def auto_label(ups, downs, labels, figure):
    for i in range(len(ups)):
        height = ups[i].get_height() + downs[i].get_height()
        plt.text(ups[i].get_x() + ups[i].get_width() / 2.0, height + 250, "%1.2f" % labels[i],
                 ha="center",
                 rotation=90,
                 fontsize=28)
        i += 1


def main():
    """
    Main Function, nothing to comment
    """
    scenario = "lan"

    file_name_base = "./LabRecord/result/fairness"

    algorithms = ["bbr", "scalable", "bic", "highspeed", "htcp", "hybla", "illinois", "vegas", "yeah"]
    names = ["BBR", "Scalable", "BIC", "High Speed", "H-TCP", "Hybla", "Illinois", "Vegas", "YeAH"]

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
            path_base = file_name_base + "/" + scenario + "/" + test + "/" + algorithm + "/"
            if test == "vs_itself":
                exp_name = names[algorithms.index(algorithm)] + "_1"
                con_name = names[algorithms.index(algorithm)] + "_2"
                exp_filename = "/" + algorithm + "_1.log"
                con_filename = "/" + algorithm + "_2.log"
                process(path_base, exp_filename, con_filename, index_itself, vs_itself_exp, vs_itself_con)
            if test == "vs_reno":
                exp_name = names[algorithms.index(algorithm)]
                con_name = "Reno"
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/reno.log"
                process(path_base, exp_filename, con_filename, index_reno, vs_reno_exp, vs_reno_con)
            if test == "vs_cubic":
                con_name = "CUBIC"
                exp_name = names[algorithms.index(algorithm)]
                exp_filename = "/" + algorithm + ".log"
                con_filename = "/cubic.log"
                process(path_base, exp_filename, con_filename, index_cubic, vs_cubic_exp, vs_cubic_con)

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

    exp_reno = plt.bar(x + 0 * width - 1.2, vs_reno_exp,
                       width=width,
                       label='Testee',
                       alpha=0.5,
                       color="red")
    exp_cubic = plt.bar(x + 1 * width - 1.2, vs_cubic_exp,
                        width=width,
                        label='Testee',
                        alpha=0.5,
                        color="blue")
    exp_itself = plt.bar(x + 2 * width - 1.2, vs_itself_exp,
                         width=width,
                         label='Testee',
                         alpha=0.5,
                         color="black")
    # Con
    con_reno = plt.bar(x + 0 * width - 1.2, vs_reno_con, bottom=vs_reno_exp, width=width,
                       label='Reno',
                       alpha=0.5,
                       color="darkorange")
    auto_label(con_reno, exp_reno, index_reno, fig)
    con_cubic = plt.bar(x + 1 * width - 1.2, vs_cubic_con, bottom=vs_cubic_exp, width=width,
                        label='CUBIC',
                        alpha=0.5,
                        color="lawngreen")
    auto_label(con_cubic, exp_cubic, index_cubic, fig)
    con_itself = plt.bar(x + 2 * width - 1.2, vs_itself_con, bottom=vs_itself_exp, width=width,
                         label='Itself',
                         alpha=0.5,
                         color="dodgerblue")
    auto_label(con_itself, exp_itself, index_itself, fig)

    # Index
    """
    for i, v in enumerate(index_reno):
        plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
    for i, v in enumerate(index_cubic):
        plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
    for i, v in enumerate(index_itself):
        plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
    
    plt.text(con_reno.get_x() + con_reno.get_width() / 2.0, 1.03 * con_reno.get_height(), index_reno)
    plt.text(con_cubic.get_x() + con_cubic.get_width() / 2.0, 1.03 * con_cubic.get_height(), index_cubic)
    plt.text(con_itself.get_x() + con_itself.get_width() / 2.0, 1.03 * con_itself.get_height(), index_itself)
"""
    plt.xticks(x + 1.5 * width - 1.2, ["BBR", "Scalable", "BIC", "High Speed", "H-TCP", "Hybla", "Illinois",
                                       "Vegas", "YeAH"], fontsize=32, rotation="45")
    plt.ylabel("Transferred Data in 300 seconds(MB)", fontsize=32)
    plt.yticks(fontsize=32)
    plt.ylim(0, numpy.max(data) * 1.8)

    plt.legend(fontsize=24)

    plt.show()

    """
    experimented = file_name_base + scenario + "/vs_itself/cubic/1/cubic_1.log"
    contrasted = file_name_base + scenario + "/vs_itself/cubic/1/cubic_2.log"

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
    """


#   Function Main
if __name__ == '__main__':
    main()
