# coding=utf-8
# filename: index.py

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


def get_index(a, b):
    result = ((a + b) * (a + b)) / (2 * (a * a + b * b))
    return result


def main():

    fsize = 36

    doc = read_text_file('./python/index.csv')

    a = []
    b = []
    index = []

    xt = np.arange(0, 105, 5)
    yt = np.arange(0.5, 1.05, 0.05)

    for i in range(len(doc)):
        line = doc[i].replace('\r\n', '')
        numbers = line.split(',')
        a.append(numbers[0])
        b.append(numbers[1])
        index.append(numbers[2])

    plt.plot(a, index, linewidth=4)

    plt.xticks(xt, fontsize=fsize, y=-0.02)
    plt.xlabel('The Percentage of Flow A', fontsize=fsize)

    plt.yticks(yt, fontsize=fsize)
    plt.ylabel('Jain`s Fairness Index', fontsize=fsize)
    plt.ylim(0.5, 1.05)

    plt.grid(True, linestyle="--", linewidth="2", alpha=0.5)
    plt.subplots_adjust(left=0.09, right=0.96, top=0.95, bottom=0.12)

    plt.show()


if __name__ == '__main__':
    main()
