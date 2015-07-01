#!/usr/bin/python

import sys
import heapq

lastTag = None
sortedList = {}

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 3:
        continue
    nouse, tag, count = datas
    if tag not in sortedList.keys():
        sortedList[tag] = 0
    sortedList[tag] += 1

results = heapq.nlargest(10, sortedList, key=sortedList.get)

for item in results:
    print '{0}\t{1}'.format(item, sortedList[item])