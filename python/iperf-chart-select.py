# coding=utf-8
# filename: iperf3-chart-select.py

import sys
import json

import matplotlib.pyplot as plt
import numpy as np

import libutil as util


def main():

    # Settings for wired scenario
    wired = {
        "algorithms": ["bbr", "scalable", "bic", "cubic", "highspeed",
                  "htcp", "hybla", "illinois", "vegas", "yeah", "reno"],
        "names": ["BBR", "Scalable", "BIC", "CUBIC", "High Speed", "H-TCP", "Hybla",
             "Illinois", "Vegas", "YeAH", "Reno"],
        "path": "../lab-record/result/fairness/lan_to_dc1/vs_cubic/",
        "round_count": 3,
        "flow_A": "bbr",
        "flow_B": "cubic",
        "length": 900
    }

    # Settings for wireless scenario
    wireless = {
        "algorithms": ["bbr", "cubic", "reno", "veno"],
        "names": ["BBR", "CUBIC", "Reno", "Veno"],
        "path": "../shell/5g/tx-5mw/",
        "round_count": 3
    }

    result = {}

    # Load result for flow A
    flow_a_intervals = []
    for i in range(1, wired["round_count"] + 1):
        path = wired["path"] + wired["flow_A"] + "/" + str(i) + "/" + wired["flow_A"] + ".log"
        json_object = json.loads("".join(util.read_json_file(path)))
        flow_a_intervals.append(util.load_interval_array(json_object["intervals"], "bits_per_second"))

    # Load result for flow B
    flow_b_intervals = []
    for i in range(1, wired["round_count"] + 1):
        path = wired["path"] + wired["flow_A"] + "/" + str(i) + "/" + wired["flow_B"] + ".log"
        json_object = json.loads("".join(util.read_json_file(path)))
        flow_b_intervals.append(util.load_interval_array(json_object["intervals"], "bits_per_second"))

    # Create x tick
    x = np.arange(0, wired["length"])

    # Plot charts for selection
    for i in range(wired["round_count"]):
        # Calculate the sum of speed
        sum_speed = []
        for j in range(wired["length"]):
            sum_speed.append(flow_a_intervals[i][j] + flow_b_intervals[i][j])

        plt.figure("round_" + str(i))
        plt.plot(x, flow_a_intervals[i])
        plt.plot(x, sum_speed)

    plt.show()

if __name__ == "__main__":
    sys.exit(main())
