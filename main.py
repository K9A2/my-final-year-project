# coding: UTF-8


"""
hjkljklj;ljljjkljkl
"""

import matplotlib.pyplot as plt
import re

txtStrings = []

keys = []

list_6 = []
list_7 = []
list_3 = []
list_4 = []
list_5 = []
list_sum = []

numberPattern = "\[(.*?)\]"
sumPattern = "\[(SUM)\]"
bandwidthPattern = "MBytes  (.*?) Mbits/sec"

txtFile = open("result.txt")
line = txtFile.readline()
while line:
    txtStrings.append(line)
    line = txtFile.readline()

txtFile.close()

bandwidth = float(str(re.findall(bandwidthPattern, txtStrings[12], re.S))[2:6])

# Get keys for each line, and store them in "keys"
for i in range(4, 9):
    result = re.findall(numberPattern, txtStrings[i], re.S)
    if result is not None:
        string = str(result)
        keys.append(int(string[2:5]))
    else:
        print "none"

'''
Currently, they start from line 10 statically.
It will be transferred to dynamic computed later.
A set of results are grouped in 5 lines starts from line 10.
For example:
    [  6] 42.0-43.0 sec  2.25 MBytes  18.9 Mbits/sec
    [  4] 42.0-43.0 sec  2.00 MBytes  16.8 Mbits/sec
    [  7] 42.0-43.0 sec  2.25 MBytes  18.9 Mbits/sec
    [  3] 42.0-43.0 sec  2.38 MBytes  19.9 Mbits/sec
    [  5] 42.0-43.0 sec  2.50 MBytes  21.0 Mbits/sec
    [SUM] 42.0-43.0 sec  11.4 MBytes  95.4 Mbits/sec
If not, breaks.
'''
i = 15
while i < len(txtStrings):
    # Starts from line 16, if line[current + 6] can not find "SUM", breaks
    singleLine = str(re.findall(sumPattern, txtStrings[i], re.S))
    if cmp(singleLine[2:5], "SUM") == 0:
        '''
        Indicating that 5 lines above is validated, therefor, put them in
        corresponding list, after append sum into its own list
        '''
        list_sum.append(float(str(re.findall(bandwidthPattern, txtStrings[i], re.S))[2:6]))
        j = i - 1
        while j > (i - 6):
            # Find ID
            line = str(re.findall(numberPattern, txtStrings[j], re.S))
            if line is not None:
                # Redirect to different lists according to their specific IDs
                ID = int(str(line[2:5]))
                if ID == 3:
                    list_3.append(float(str(re.findall(bandwidthPattern, txtStrings[j], re.S))[2:6]))
                elif ID == 4:
                    list_4.append(float(str(re.findall(bandwidthPattern, txtStrings[j], re.S))[2:6]))
                elif ID == 5:
                    list_5.append(float(str(re.findall(bandwidthPattern, txtStrings[j], re.S))[2:6]))
                elif ID == 6:
                    list_6.append(float(str(re.findall(bandwidthPattern, txtStrings[j], re.S))[2:6]))
                elif ID == 7:
                    list_7.append(float(str(re.findall(bandwidthPattern, txtStrings[j], re.S))[2:6]))
            j -= 1
    else:
        break
    i += 6

list_y = []

for i in range(len(list_sum)):
    list_y.append(i)

x3 = list_3

x4 = list_4

x5 = list_5

x6 = list_6

x7 = list_7

plt.title('broadcast(b) vs join(r)')
plt.xlabel('time(s)')
plt.ylabel('data size(Mbit\s)')

plt.plot(list_y, x3, 'red', label='f3', linewidth=2.0)
plt.plot(list_y, x4, 'green', label='f4', linewidth=2.0)
plt.plot(list_y, x5, 'blue', label='f5', linewidth=2.0)
plt.plot(list_y, x6, 'black', label='f6', linewidth=2.0)
plt.plot(list_y, x7, 'grey', label='f7', linewidth=2.0)

plt.legend(bbox_to_anchor=[0.3, 1])
plt.grid()
plt.show()
