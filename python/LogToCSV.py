import json
import re

import benchmark


def print_to_csv(result, keys):
    file_name = "./result.csv"
    f = open(file_name, "w")

    for i in range(len(keys)):
        rtt = result[keys[i]]["rtt"]
        bandwidth = result[keys[i]]["bits_per_second"]
        retr = result[keys[i]]["retransmits"]
        for j in range(len(rtt)):
            f.write(str(rtt[j]) + "," + str(bandwidth[j]) + "," +
                    str(retr[j]) + "\n")

    f.close()


def main():
    """
    Main Function, nothing to comment
    """
    #   Load and parse json object from file with specific
    file_name = "./benchmark.log"
    doc = re.sub("[\n|\t]", "", "".join(benchmark.read_text_file(file_name)))
    json_object = json.loads("".join(doc))

    intervals = json_object["intervals"]

    socket_keys = benchmark.get_socket_keys(intervals)

    result = benchmark.get_result_dictionary(intervals, socket_keys)

    print_to_csv(result, socket_keys)


#   Function Main
if __name__ == '__main__':
    main()
