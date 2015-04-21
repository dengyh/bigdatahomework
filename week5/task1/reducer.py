#!/usr/bin/python

import sys

totalLength = 0
totalCount = 0

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    key, countTuple = datas
    length, count = map(int, eval(countTuple))
    totalLength += length
    totalCount += count

print totalLength * 1.0 / totalCount