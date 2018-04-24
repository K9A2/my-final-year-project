# coding=utf-8
# filename: libutil.py


def read_json_file(file_name):
    """
    Read experiment result in text file

    :param file_name:   File path to result file
    :return:    Data text in list, line by line
    """
    target_file = open(file_name)
    lines = target_file.readlines()

    target_file.close()
    return lines


def load_interval_array(intervals, name):
    array = []
    for i in range(len(intervals)):
        array.append(intervals[i]["streams"][0][name] / (1000.0 * 1000.0))
    return array
