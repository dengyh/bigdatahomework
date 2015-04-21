#!/usr/bin/python

import sys
import heapq

samples = []

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    key, price = datas
    heapq.heappush(samples, float(price))

print samples[len(samples) / 2]